"""Tests that publish file plugin repositories."""
import pytest

from pulp_smash.pulp3.bindings import monitor_task

from pulpcore.client.pulp_file import (
    RepositorySyncURL,
    FileFilePublication,
)
from pulpcore.client.pulp_file.exceptions import ApiException


@pytest.mark.parallel
def test_creating_publications(
    file_repo,
    file_fixture_gen_remote_ssl,
    file_repo_api_client,
    file_pub_api_client,
    basic_manifest_path,
    gen_object_with_cleanup,
    file_random_content_unit,
):
    # Tests that a publication can be created from a specific repository version
    remote = file_fixture_gen_remote_ssl(manifest_path=basic_manifest_path, policy="on_demand")

    # Sync from the remote
    body = RepositorySyncURL(remote=remote.pulp_href)
    monitor_task(file_repo_api_client.sync(file_repo.pulp_href, body).task)
    first_repo_version_href = file_repo_api_client.read(file_repo.pulp_href).latest_version_href
    assert first_repo_version_href.endswith("/versions/1/")

    # Add a new content unit to the repository and assert that a new repository version is created
    monitor_task(
        file_repo_api_client.modify(
            file_repo.pulp_href, {"add_content_units": [file_random_content_unit.pulp_href]}
        ).task
    )
    file_repo = file_repo_api_client.read(file_repo.pulp_href)
    assert file_repo.latest_version_href.endswith("/versions/2/")

    # Create a Publication using a repository and assert that its repository_version is the latest
    publish_data = FileFilePublication(repository=file_repo.pulp_href)
    publication = gen_object_with_cleanup(file_pub_api_client, publish_data)
    assert publication.repository_version == file_repo.latest_version_href
    assert publication.manifest == "PULP_MANIFEST"

    # Create a Publication using a non-latest repository version
    publish_data = FileFilePublication(repository_version=first_repo_version_href)
    publication = gen_object_with_cleanup(file_pub_api_client, publish_data)
    assert publication.repository_version == first_repo_version_href

    # Assert that a publication can't be created by specifying a repository and a repo version
    publish_data = FileFilePublication(
        repository=file_repo.pulp_href, repository_version=first_repo_version_href
    )
    with pytest.raises(ApiException) as exc:
        gen_object_with_cleanup(file_pub_api_client, publish_data)
    assert exc.value.status == 400

    # Assert that a Publication can be created using a custom manifest
    publish_data = FileFilePublication(repository=file_repo.pulp_href, manifest="listing")
    publication = gen_object_with_cleanup(file_pub_api_client, publish_data)
    assert publication.manifest == "listing"
