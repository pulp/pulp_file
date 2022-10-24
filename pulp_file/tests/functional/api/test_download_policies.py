"""Tests for Pulp`s download policies."""
from aiohttp.client_exceptions import ClientResponseError
import hashlib
import os
import pytest
import uuid
from urllib.parse import urljoin

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import (
    get_added_content_summary,
    get_content_summary,
)

from pulp_file.tests.functional.utils import get_files_in_manifest, download_file

from pulpcore.app import settings
from pulpcore.client.pulp_file import FileFilePublication, RepositorySyncURL


OBJECT_STORAGES = (
    "storages.backends.s3boto3.S3Boto3Storage",
    "storages.backends.azure_storage.AzureStorage",
)


def _do_range_request_download_and_assert(url, range_header, expected_bytes):
    file1 = download_file(url, headers=range_header)
    file2 = download_file(url, headers=range_header)
    assert expected_bytes == len(file1.body)
    assert expected_bytes == len(file2.body)
    assert file1.body == file2.body

    assert file1.response_obj.status == 206
    assert file1.response_obj.status == file2.response_obj.status

    assert str(expected_bytes) == file1.response_obj.headers["Content-Length"]
    assert str(expected_bytes) == file2.response_obj.headers["Content-Length"]

    assert (
        file1.response_obj.headers["Content-Range"] == file2.response_obj.headers["Content-Range"]
    )


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
    range_header_manifest_path,
    gen_object_with_cleanup,
    file_content_api_client,
    download_policy,
):
    """Test that "on_demand" and "streamed" download policies work as expected."""
    remote = file_fixture_gen_remote_ssl(
        manifest_path=range_header_manifest_path, policy=download_policy
    )
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

    # Create a Distribution
    distribution = gen_object_with_cleanup(
        file_distro_api_client,
        {
            "name": str(uuid.uuid4()),
            "base_path": str(uuid.uuid4()),
            "repository": file_repo.pulp_href,
        },
    )

    # Assert that un-published content is not available
    for expected_file in expected_files:
        with pytest.raises(ClientResponseError) as exc:
            content_unit_url = urljoin(distribution.base_url, expected_file[1])
            download_file(content_unit_url)
        assert exc.value.code == 404

    # Create a File Publication and assert that the repository_version is set on the Publication.
    publish_data = FileFilePublication(repository=file_repo.pulp_href)
    publication = gen_object_with_cleanup(file_pub_api_client, publish_data)
    assert publication.repository_version is not None

    # Download one of the files and assert that it has the right checksum
    expected_files_list = list(expected_files)
    content_unit = expected_files_list[0]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    downloaded_file = download_file(content_unit_url)
    actual_checksum = hashlib.sha256(downloaded_file.body).hexdigest()
    expected_checksum = content_unit[1]
    assert expected_checksum == actual_checksum
    if download_policy == "immediate" and settings.DEFAULT_FILE_STORAGE in OBJECT_STORAGES:
        content_disposition = downloaded_file.response_obj.headers.get("Content-Disposition")
        assert content_disposition is not None
        filename = os.path.basename(content_unit[0])
        assert f"attachment;filename={filename}" == content_disposition

    # Assert proper download with range requests smaller than one chunk of downloader
    range_header = {"Range": "bytes=1048586-1049586"}
    num_bytes = 1001
    content_unit = expected_files_list[1]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    _do_range_request_download_and_assert(content_unit_url, range_header, num_bytes)

    # Assert proper download with range requests spanning multiple chunks of downloader
    range_header = {"Range": "bytes=1048176-2248576"}
    num_bytes = 1200401
    content_unit = expected_files_list[2]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    _do_range_request_download_and_assert(content_unit_url, range_header, num_bytes)

    # Assert that multiple requests with different Range header values work as expected
    range_header = {"Range": "bytes=1048176-2248576"}
    num_bytes = 1200401
    content_unit = expected_files_list[3]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    _do_range_request_download_and_assert(content_unit_url, range_header, num_bytes)

    range_header = {"Range": "bytes=2042176-3248576"}
    num_bytes = 1206401
    content_unit = expected_files_list[3]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    _do_range_request_download_and_assert(content_unit_url, range_header, num_bytes)

    # Assert that range requests with a negative start value errors as expected
    content_unit = expected_files_list[4]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    # The S3 test API project doesn't handle invalid Range values correctly
    if settings.DEFAULT_FILE_STORAGE == "pulpcore.app.models.storage.FileSystem":
        with pytest.raises(ClientResponseError) as exc:
            range_header = {"Range": "bytes=-1-11"}
            download_file(content_unit_url, headers=range_header)
        assert exc.value.code == 416

    # Assert that a range request with a start value larger than the content errors
    content_unit = expected_files_list[5]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    with pytest.raises(ClientResponseError) as exc:
        range_header = {"Range": "bytes=10485860-10485870"}
        download_file(content_unit_url, headers=range_header)
    assert exc.value.code == 416

    # Assert that a range request with an end value that is larger than the data works
    range_header = {"Range": "bytes=4193804-4294304"}
    num_bytes = 500
    content_unit = expected_files_list[6]
    content_unit_url = urljoin(distribution.base_url, content_unit[0])
    _do_range_request_download_and_assert(content_unit_url, range_header, num_bytes)

    # Assert that artifacts were not downloaded if policy is not immediate
    if download_policy != "immediate":
        # Assert that artifacts were not downloaded
        content_unit = expected_files_list[7]
        assert artifacts_api_client.list(sha256=content_unit[1]).results == []

        # Assert that an artifact was saved for the "on_demand" policy and not saved for the
        # "streamed" policy. Only check the first content unit because Range requests don't
        # cause the artifact to be saved. https://github.com/pulp/pulpcore/issues/3060
        content_unit = expected_files_list[0]
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
