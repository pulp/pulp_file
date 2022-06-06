"""Tests that perform actions over content unit."""
import uuid

import pytest

from pulp_smash.pulp3.bindings import (
    monitor_task,
    PulpTaskError,
)


@pytest.mark.parallel
def test_crud_content_unit(
    random_artifact, file_random_content_unit, file_content_api_client, gen_object_with_cleanup
):
    artifact_attrs = {"artifact": random_artifact.pulp_href, "relative_path": str(uuid.uuid4())}
    content_unit = gen_object_with_cleanup(file_content_api_client, **artifact_attrs)
    assert content_unit.artifact == random_artifact.pulp_href
    assert content_unit.relative_path == artifact_attrs["relative_path"]

    response = file_content_api_client.list(relative_path=content_unit.relative_path)
    assert response.count == 1

    content_unit = file_content_api_client.read(content_unit.pulp_href)
    assert content_unit.artifact == random_artifact.pulp_href
    assert content_unit.relative_path == artifact_attrs["relative_path"]

    with pytest.raises(AttributeError) as exc:
        file_content_api_client.partial_update(
            content_unit.pulp_href, relative_path=str(uuid.uuid())
        )
    assert exc.value.args[0] == "'ContentFilesApi' object has no attribute 'partial_update'"

    with pytest.raises(AttributeError) as exc:
        file_content_api_client.update(content_unit.pulp_href, relative_path=str(uuid.uuid()))
    assert exc.value.args[0] == "'ContentFilesApi' object has no attribute 'update'"


@pytest.mark.parallel
def test_same_sha256_same_relative_path_not_allowed(
    random_artifact, file_content_api_client, gen_object_with_cleanup
):
    artifact_attrs = {"artifact": random_artifact.pulp_href, "relative_path": str(uuid.uuid4())}
    gen_object_with_cleanup(file_content_api_client, **artifact_attrs)

    with pytest.raises(PulpTaskError):
        gen_object_with_cleanup(file_content_api_client, **artifact_attrs)


@pytest.mark.parallel
def test_same_sha256_diff_relative_path(
    random_artifact, file_content_api_client, gen_object_with_cleanup
):
    artifact_attrs = {"artifact": random_artifact.pulp_href, "relative_path": str(uuid.uuid4())}
    gen_object_with_cleanup(file_content_api_client, **artifact_attrs)

    artifact_attrs["relative_path"] = str(uuid.uuid4())
    artifact_attrs = {"artifact": random_artifact.pulp_href, "relative_path": str(uuid.uuid4())}
    gen_object_with_cleanup(file_content_api_client, **artifact_attrs)

    response = file_content_api_client.list(relative_path=artifact_attrs["relative_path"])
    assert response.count == 1


@pytest.mark.parallel
def test_second_content_unit_with_same_rel_path_replaces_the_first(
    file_repo,
    random_artifact_factory,
    file_content_api_client,
    gen_object_with_cleanup,
    file_repo_ver_api_client,
    file_repo_api_client,
):
    latest_repo_version = file_repo_ver_api_client.read(file_repo.latest_version_href)
    assert latest_repo_version.number == 0

    artifact_attrs = {
        "artifact": random_artifact_factory().pulp_href,
        "relative_path": str(uuid.uuid4()),
        "repository": file_repo.pulp_href,
    }
    gen_object_with_cleanup(file_content_api_client, **artifact_attrs)

    file_repo = file_repo_api_client.read(file_repo.pulp_href)
    latest_repo_version = file_repo_ver_api_client.read(file_repo.latest_version_href)
    assert latest_repo_version.content_summary.present["file.file"]["count"] == 1
    assert latest_repo_version.number == 1

    artifact_attrs["artifact"] = random_artifact_factory().pulp_href
    gen_object_with_cleanup(file_content_api_client, **artifact_attrs)

    file_repo = file_repo_api_client.read(file_repo.pulp_href)
    latest_repo_version = file_repo_ver_api_client.read(file_repo.latest_version_href)
    assert latest_repo_version.content_summary.present["file.file"]["count"] == 1
    assert latest_repo_version.number == 2


@pytest.mark.parallel
def test_cannot_create_repo_version_with_two_relative_paths_the_same(
    file_repo,
    random_artifact_factory,
    file_content_api_client,
    gen_object_with_cleanup,
    file_repo_ver_api_client,
    file_repo_api_client,
):
    latest_repo_version = file_repo_ver_api_client.read(file_repo.latest_version_href)
    assert latest_repo_version.number == 0

    artifact_attrs = {
        "artifact": random_artifact_factory().pulp_href,
        "relative_path": str(uuid.uuid4()),
    }
    first_content_unit = gen_object_with_cleanup(file_content_api_client, **artifact_attrs)

    artifact_attrs["artifact"] = random_artifact_factory().pulp_href
    second_content_unit = gen_object_with_cleanup(file_content_api_client, **artifact_attrs)

    response = file_content_api_client.list(relative_path=first_content_unit.relative_path)
    assert response.count == 2

    data = {"add_content_units": [first_content_unit.pulp_href, second_content_unit.pulp_href]}

    with pytest.raises(PulpTaskError):
        response = file_repo_api_client.modify(file_repo.pulp_href, data)
        monitor_task(response.task)
