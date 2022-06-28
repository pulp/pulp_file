"""Tests for Pulp`s download policies."""
import pytest

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import (
    get_added_content_summary,
    get_content_summary,
)

from pulp_file.tests.functional.utils import get_files_in_manifest

from pulpcore.client.pulp_file import FileFilePublication, RepositorySyncURL


@pytest.mark.parallel
@pytest.mark.parametrize("download_policy", ["on_demand", "streamed"])
def test_download_policy(
    artifacts_api_client,
    file_repo,
    file_fixture_gen_remote_ssl,
    file_remote_api_client,
    file_repo_api_client,
    file_pub_api_client,
    basic_manifest_path,
    gen_object_with_cleanup,
    file_content_api_client,
    download_policy,
):
    """Test that "on_demand" and "streamed" download policies work as expected."""
    remote = file_fixture_gen_remote_ssl(manifest_path=basic_manifest_path, policy=download_policy)
    file_repo = file_repo_api_client.read(file_repo.pulp_href)
    assert file_repo.latest_version_href.endswith("/versions/0/")

    # Check what content and artifacts are in the fixture repository
    expected_files = get_files_in_manifest(remote.url)

    # Sync from the remote and assert that a new repository version is created
    body = RepositorySyncURL(remote=remote.pulp_href)
    monitor_task(file_repo_api_client.sync(file_repo.pulp_href, body).task)
    file_repo = file_repo_api_client.read(file_repo.pulp_href)
    assert file_repo.latest_version_href.endswith("/versions/1/")
    assert get_content_summary(file_repo.to_dict()) == {"file.file": len(expected_files)}
    assert get_added_content_summary(file_repo.to_dict()) == {"file.file": len(expected_files)}

    # Sync again and assert that nothing changes
    latest_version_href = file_repo.latest_version_href
    monitor_task(file_repo_api_client.sync(file_repo.pulp_href, body).task)
    file_repo = file_repo_api_client.read(file_repo.pulp_href)
    assert latest_version_href == file_repo.latest_version_href
    assert get_content_summary(file_repo.to_dict()) == {"file.file": len(expected_files)}

    # Assert that no HTTP error was raised when list on_demand content
    content = file_content_api_client.list(
        repository_version=file_repo.latest_version_href
    ).to_dict()["results"]
    assert len(content) == len(expected_files)

    # Assert that artifacts were not downloaded
    for f in expected_files:
        assert artifacts_api_client.list(sha256=f[1]).results == []

    # Create a File Publication and assert that the repository_version is set on the Publication.
    publish_data = FileFilePublication(repository=file_repo.pulp_href)
    publication = gen_object_with_cleanup(file_pub_api_client, publish_data)
    assert publication.repository_version is not None

    # Change download policy to immediate
    response = file_remote_api_client.partial_update(remote.pulp_href, {"policy": "immediate"})
    monitor_task(response.task)
    remote = file_remote_api_client.read(remote.pulp_href)
    assert remote.policy == "immediate"

    # Sync from the remote and assert that artifacts are downloaded
    monitor_task(file_repo_api_client.sync(file_repo.pulp_href, body).task)
    for f in expected_files:
        assert len(artifacts_api_client.list(sha256=f[1]).results) == 1
