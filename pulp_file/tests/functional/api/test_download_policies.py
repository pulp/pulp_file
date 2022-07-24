"""Tests for Pulp`s download policies."""
import hashlib
import pytest
import uuid
from urllib.parse import urljoin

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import (
    get_added_content_summary,
    get_content_summary,
)

from pulp_file.tests.functional.utils import get_files_in_manifest, download_file

from pulpcore.client.pulp_file import FileFilePublication, RepositorySyncURL


@pytest.mark.parallel
@pytest.mark.parametrize("download_policy", ["immediate", "on_demand", "streamed"])
def test_download_policy(
    artifacts_api_client,
    file_repo,
    file_fixture_gen_remote_ssl,
    file_remote_api_client,
    file_repo_api_client,
    file_pub_api_client,
    file_distro_api_client,
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

    # Create a File Publication and assert that the repository_version is set on the Publication.
    publish_data = FileFilePublication(repository=file_repo.pulp_href)
    publication = gen_object_with_cleanup(file_pub_api_client, publish_data)
    assert publication.repository_version is not None

    # Create a Distribution
    distribution = gen_object_with_cleanup(
        file_distro_api_client,
        {
            "name": str(uuid.uuid4()),
            "base_path": str(uuid.uuid4()),
            "repository": file_repo.pulp_href,
        },
    )

    # Download one of the files and assert that it has the right checksum
    expected_files_list = list(expected_files)
    content_unit = expected_files_list[0]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    downloaded_file = download_file(content_unit_url)
    actual_checksum = hashlib.sha256(downloaded_file).hexdigest()
    expected_checksum = content_unit[1]
    assert expected_checksum == actual_checksum

    # Assert that artifacts were not downloaded if policy is not immediate
    if download_policy != "immediate":
        # Assert that artifacts were not downloaded
        for f in expected_files_list[1:]:
            assert artifacts_api_client.list(sha256=f[1]).results == []

        # Assert that an artifact was saved for the "on_demand" policy and not saved for the
        # "streamed" policy.
        if download_policy == "on_demand":
            assert len(artifacts_api_client.list(sha256=content_unit[1]).results) == 1
        else:
            assert len(artifacts_api_client.list(sha256=content_unit[1]).results) == 0

        # Change download policy to immediate
        response = file_remote_api_client.partial_update(remote.pulp_href, {"policy": "immediate"})
        monitor_task(response.task)
        remote = file_remote_api_client.read(remote.pulp_href)
        assert remote.policy == "immediate"

        # Sync from the remote and assert that artifacts are downloaded
        monitor_task(file_repo_api_client.sync(file_repo.pulp_href, body).task)
        for f in expected_files:
            assert len(artifacts_api_client.list(sha256=f[1]).results) == 1
