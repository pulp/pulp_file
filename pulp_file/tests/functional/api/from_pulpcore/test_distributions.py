"""Tests that perform actions over distributions."""
import pytest
import json
from uuid import uuid4

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import (
    gen_distribution,
)

from pulpcore.client.pulp_file import (
    RepositorySyncURL,
    FileFilePublication,
)
from pulpcore.client.pulp_file.exceptions import ApiException


@pytest.mark.parallel
def test_crud_publication_distribution(
    file_content_api_client,
    file_repo,
    file_fixture_gen_remote_ssl,
    file_repo_api_client,
    file_repo_ver_api_client,
    file_pub_api_client,
    basic_manifest_path,
    gen_object_with_cleanup,
    file_distro_api_client,
):
    # Create a remote and sync from it to create the first repository version
    remote = file_fixture_gen_remote_ssl(manifest_path=basic_manifest_path, policy="on_demand")
    body = RepositorySyncURL(remote=remote.pulp_href)
    monitor_task(file_repo_api_client.sync(file_repo.pulp_href, body).task)

    # Remove content to create two more repository versions
    first_repo_version_href = file_repo_api_client.read(file_repo.pulp_href).latest_version_href
    v1_content = file_content_api_client.list(repository_version=first_repo_version_href).results

    for i in range(2):
        monitor_task(
            file_repo_api_client.modify(
                file_repo.pulp_href, {"remove_content_units": [v1_content[i].pulp_href]}
            ).task
        )

    # Create a publication from version 2
    repo_versions = file_repo_ver_api_client.list(file_repo.pulp_href).results
    publish_data = FileFilePublication(repository_version=repo_versions[2].pulp_href)
    publication = gen_object_with_cleanup(file_pub_api_client, publish_data)
    distribution_data = gen_distribution(publication=publication.pulp_href)
    distribution = gen_object_with_cleanup(file_distro_api_client, distribution_data)

    # Refresh the publication data
    publication = file_pub_api_client.read(publication.pulp_href)

    # Assert on all the field values
    assert distribution.content_guard is None
    assert distribution.repository is None
    assert distribution.publication == publication.pulp_href
    assert distribution.base_path == distribution_data["base_path"]
    assert distribution.name == distribution_data["name"]

    # Assert that the publication has a reference to the distribution
    assert publication.distributions[0] == distribution.pulp_href

    # Test updating name with 'partial_update'
    new_name = str(uuid4())
    monitor_task(
        file_distro_api_client.partial_update(distribution.pulp_href, {"name": new_name}).task
    )
    distribution = file_distro_api_client.read(distribution.pulp_href)
    assert distribution.name == new_name

    # Test updating base_path with 'partial_update'
    new_base_path = str(uuid4())
    monitor_task(
        file_distro_api_client.partial_update(
            distribution.pulp_href, {"base_path": new_base_path}
        ).task
    )
    distribution = file_distro_api_client.read(distribution.pulp_href)
    assert distribution.base_path == new_base_path

    # Test updating name with 'update'
    new_name = str(uuid4())
    distribution.name = new_name
    monitor_task(file_distro_api_client.update(distribution.pulp_href, distribution).task)
    distribution = file_distro_api_client.read(distribution.pulp_href)
    assert distribution.name == new_name

    # Test updating base_path with 'update'
    new_base_path = str(uuid4())
    distribution.base_path = new_base_path
    monitor_task(file_distro_api_client.update(distribution.pulp_href, distribution).task)
    distribution = file_distro_api_client.read(distribution.pulp_href)
    assert distribution.base_path == new_base_path

    # Test the generic distribution list endpoint.
    distributions = file_distro_api_client.list()
    assert distribution.pulp_href in [distro.pulp_href for distro in distributions.results]

    # Delete a distribution.
    file_distro_api_client.delete(distribution.pulp_href)
    with pytest.raises(ApiException):
        file_distro_api_client.read(distribution.pulp_href)


def _create_distribution_and_assert(client, data):
    with pytest.raises(ApiException) as exc:
        client.create(data)
    assert json.loads(exc.value.body)["base_path"] is not None


def _update_distribution_and_assert(client, distribution_href, data):
    with pytest.raises(ApiException) as exc:
        client.update(distribution_href, data)
    assert json.loads(exc.value.body)["base_path"] is not None


@pytest.mark.parallel
def test_distribution_base_path(
    gen_object_with_cleanup,
    file_distro_api_client,
):
    distribution_data = gen_distribution(base_path=str(uuid4()).replace("-", "/"))
    distribution = gen_object_with_cleanup(file_distro_api_client, distribution_data)

    # Test that spaces can not be part of ``base_path``.
    _create_distribution_and_assert(
        file_distro_api_client, gen_distribution(base_path=str(uuid4()).replace("-", " "))
    )

    # Test that slash cannot be in the begin of ``base_path``.
    _create_distribution_and_assert(
        file_distro_api_client, gen_distribution(base_path=f"/{str(uuid4())}")
    )
    _update_distribution_and_assert(
        file_distro_api_client,
        distribution.pulp_href,
        gen_distribution(base_path=f"/{str(uuid4())}"),
    )

    # Test that slash cannot be in the end of ``base_path``."""
    _create_distribution_and_assert(
        file_distro_api_client, gen_distribution(base_path=f"{str(uuid4())}/")
    )

    _update_distribution_and_assert(
        file_distro_api_client,
        distribution.pulp_href,
        gen_distribution(base_path=f"{str(uuid4())}/"),
    )

    # Test that ``base_path`` can not be duplicated.
    _create_distribution_and_assert(
        file_distro_api_client, gen_distribution(base_path=distribution.base_path)
    )

    # Test that distributions can't have overlapping ``base_path``.
    base_path = distribution.base_path.rsplit("/", 1)[0]
    _create_distribution_and_assert(file_distro_api_client, gen_distribution(base_path=base_path))

    base_path = "/".join((distribution.base_path, str(uuid4()).replace("-", "/")))
    _create_distribution_and_assert(file_distro_api_client, gen_distribution(base_path=base_path))
