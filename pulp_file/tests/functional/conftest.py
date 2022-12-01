import logging
import os
import uuid
from collections import defaultdict
from pathlib import Path

import aiofiles
import pytest
from aiohttp import web
from pulp_smash.pulp3.utils import gen_repo
from pulpcore.client.pulp_file import (
    AcsFileApi,
    ApiClient,
    ContentFilesApi,
    DistributionsFileApi,
    FileFileAlternateContentSource,
    PublicationsFileApi,
    RemotesFileApi,
    RepositoriesFileApi,
    RepositoriesFileVersionsApi,
)

from pulp_file.tests.functional.utils import gen_file_client, generate_iso, generate_manifest

_logger = logging.getLogger(__name__)


def pytest_check_for_leftover_pulp_objects(config):
    file_client = gen_file_client()

    types_to_check = [FileFileAlternateContentSource(file_client)]
    for type_to_check in types_to_check:
        if type_to_check.list().count > 0:
            raise Exception(f"This test left over a {type_to_check}.")


# Api Bindings fixtures


@pytest.fixture(scope="session")
def file_client(_api_client_set, bindings_cfg):
    api_client = ApiClient(bindings_cfg)
    _api_client_set.add(api_client)
    yield api_client
    _api_client_set.remove(api_client)


@pytest.fixture(scope="session")
def file_acs_api_client(file_client):
    return AcsFileApi(file_client)


@pytest.fixture(scope="session")
def file_content_api_client(file_client):
    return ContentFilesApi(file_client)


@pytest.fixture(scope="session")
def file_distro_api_client(file_client):
    return DistributionsFileApi(file_client)


@pytest.fixture(scope="session")
def file_pub_api_client(file_client):
    return PublicationsFileApi(file_client)


@pytest.fixture(scope="session")
def file_repo_api_client(file_client):
    return RepositoriesFileApi(file_client)


@pytest.fixture(scope="session")
def file_repo_ver_api_client(file_client):
    return RepositoriesFileVersionsApi(file_client)


@pytest.fixture(scope="session")
def file_remote_api_client(file_client):
    return RemotesFileApi(file_client)


# Factory fixtures


@pytest.fixture
def file_random_content_unit(file_content_unit_with_name_factory):
    return file_content_unit_with_name_factory(str(uuid.uuid4()))


@pytest.fixture
def file_content_unit_with_name_factory(file_content_api_client, random_artifact, monitor_task):
    def _file_content_unit_with_name_factory(name):
        artifact_attrs = {"artifact": random_artifact.pulp_href, "relative_path": name}
        return file_content_api_client.read(
            monitor_task(file_content_api_client.create(**artifact_attrs).task).created_resources[0]
        )

    return _file_content_unit_with_name_factory


@pytest.fixture
def file_repo(file_repo_api_client, gen_object_with_cleanup):
    return gen_object_with_cleanup(file_repo_api_client, gen_repo())


@pytest.fixture
def file_repo_with_auto_publish(file_repo_api_client, gen_object_with_cleanup):
    return gen_object_with_cleanup(file_repo_api_client, gen_repo(autopublish=True))


@pytest.fixture
def file_distribution_factory(file_distro_api_client, gen_object_with_cleanup):
    def _file_distribution_factory(**kwargs):
        data = {"base_path": str(uuid.uuid4()), "name": str(uuid.uuid4())}
        data.update(kwargs)
        return gen_object_with_cleanup(file_distro_api_client, data)

    return _file_distribution_factory


@pytest.fixture
def file_fixtures_root(tmpdir):
    return Path(tmpdir)


@pytest.fixture
def write_3_iso_file_fixture_data_factory(file_fixtures_root):
    def _write_3_iso_file_fixture_data_factory(name):
        file_fixtures_root.joinpath(name).mkdir()
        file1 = generate_iso(file_fixtures_root.joinpath(f"{name}/1.iso"))
        file2 = generate_iso(file_fixtures_root.joinpath(f"{name}/2.iso"))
        file3 = generate_iso(file_fixtures_root.joinpath(f"{name}/3.iso"))
        generate_manifest(
            file_fixtures_root.joinpath(f"{name}/PULP_MANIFEST"), [file1, file2, file3]
        )
        return f"/{name}/PULP_MANIFEST"

    return _write_3_iso_file_fixture_data_factory


@pytest.fixture
def basic_manifest_path(write_3_iso_file_fixture_data_factory):
    return write_3_iso_file_fixture_data_factory("basic")


@pytest.fixture
def copy_manifest_only_factory(file_fixtures_root):
    def _copy_manifest_only(name):
        file_fixtures_root.joinpath(f"{name}-manifest").mkdir()
        src = file_fixtures_root.joinpath(f"{name}/PULP_MANIFEST")
        dst = file_fixtures_root.joinpath(f"{name}-manifest/PULP_MANIFEST")
        os.symlink(src, dst)
        return f"/{name}-manifest/PULP_MANIFEST"

    return _copy_manifest_only


@pytest.fixture
def basic_manifest_only_path(copy_manifest_only_factory):
    return copy_manifest_only_factory("basic")


@pytest.fixture
def large_manifest_path(file_fixtures_root):
    one_megabyte = 1048576
    file_fixtures_root.joinpath("large").mkdir()
    file1 = generate_iso(file_fixtures_root.joinpath("large/1.iso"), 10 * one_megabyte)
    generate_manifest(file_fixtures_root.joinpath("large/PULP_MANIFEST"), [file1])
    return "/large/PULP_MANIFEST"


@pytest.fixture
def range_header_manifest_path(file_fixtures_root):
    """A path to a File repository manifest that contains 8 unique files each 4mb in size."""
    one_megabyte = 1048576
    file_fixtures_root.joinpath("range/foo").mkdir(parents=True)
    files = [
        generate_iso(
            file_fixtures_root.joinpath(f"range/foo/{i}.iso"), 4 * one_megabyte, f"foo/{i}.iso"
        )
        for i in range(8)
    ]

    generate_manifest(
        file_fixtures_root.joinpath("range/PULP_MANIFEST"),
        files,
    )
    return "/range/PULP_MANIFEST"


@pytest.fixture
def manifest_path_with_commas(file_fixtures_root):
    file_fixtures_root.joinpath("comma_test").mkdir()
    file_fixtures_root.joinpath("comma_test/comma,folder").mkdir()
    file_fixtures_root.joinpath("comma_test/basic_folder").mkdir()
    file1 = generate_iso(file_fixtures_root.joinpath("comma_test/comma,folder/,comma,,file,.iso"))
    file2 = generate_iso(file_fixtures_root.joinpath("comma_test/comma,folder/basic_file.iso"))
    file3 = generate_iso(file_fixtures_root.joinpath("comma_test/basic_folder/comma,file.iso"))
    generate_manifest(
        file_fixtures_root.joinpath("comma_test/PULP_MANIFEST"), [file1, file2, file3]
    )
    return "/comma_test/PULP_MANIFEST"


@pytest.fixture
def invalid_manifest_path(file_fixtures_root, basic_manifest_path):
    file_path_to_corrupt = file_fixtures_root / Path("basic/1.iso")
    with open(file_path_to_corrupt, "w") as f:
        f.write("this is not the right data")
    return basic_manifest_path


@pytest.fixture
def duplicate_filename_paths(write_3_iso_file_fixture_data_factory):
    return (
        write_3_iso_file_fixture_data_factory("file"),
        write_3_iso_file_fixture_data_factory("file2"),
    )


@pytest.fixture
def file_fixture_server_ssl_client_cert_req(
    ssl_ctx_req_client_auth, file_fixtures_root, gen_fixture_server
):
    yield gen_fixture_server(file_fixtures_root, ssl_ctx_req_client_auth)


@pytest.fixture
def file_fixture_server_ssl(ssl_ctx, file_fixtures_root, gen_fixture_server):
    yield gen_fixture_server(file_fixtures_root, ssl_ctx)


@pytest.fixture
def file_fixture_server(file_fixtures_root, gen_fixture_server):
    yield gen_fixture_server(file_fixtures_root, None)


@pytest.fixture
def file_fixture_gen_remote(file_fixture_server, file_remote_api_client, gen_object_with_cleanup):
    def _file_fixture_gen_remote(*, manifest_path, policy, **kwargs):
        url = file_fixture_server.make_url(manifest_path)
        kwargs.update({"url": str(url), "policy": policy, "name": str(uuid.uuid4())})
        return gen_object_with_cleanup(file_remote_api_client, kwargs)

    yield _file_fixture_gen_remote


@pytest.fixture
def file_fixture_gen_remote_ssl(
    file_fixture_server_ssl,
    file_remote_api_client,
    tls_certificate_authority_cert,
    gen_object_with_cleanup,
):
    def _file_fixture_gen_remote_ssl(*, manifest_path, policy, **kwargs):
        url = file_fixture_server_ssl.make_url(manifest_path)
        kwargs.update(
            {
                "url": str(url),
                "policy": policy,
                "name": str(uuid.uuid4()),
                "ca_cert": tls_certificate_authority_cert,
            }
        )
        return gen_object_with_cleanup(file_remote_api_client, kwargs)

    yield _file_fixture_gen_remote_ssl


@pytest.fixture
def file_fixture_gen_remote_client_cert_req(
    file_fixture_server_ssl_client_cert_req,
    file_remote_api_client,
    tls_certificate_authority_cert,
    client_tls_certificate_cert_pem,
    client_tls_certificate_key_pem,
    gen_object_with_cleanup,
):
    def _file_fixture_gen_remote_client_cert_req(*, manifest_path, policy, **kwargs):
        url = file_fixture_server_ssl_client_cert_req.make_url(manifest_path)
        kwargs.update(
            {
                "url": str(url),
                "policy": policy,
                "name": str(uuid.uuid4()),
                "ca_cert": tls_certificate_authority_cert,
                "client_cert": client_tls_certificate_cert_pem,
                "client_key": client_tls_certificate_key_pem,
            }
        )
        return gen_object_with_cleanup(file_remote_api_client, kwargs)

    yield _file_fixture_gen_remote_client_cert_req


@pytest.fixture
def file_fixture_gen_file_repo(file_repo_api_client, gen_object_with_cleanup):
    """A factory to generate a File Repository with auto-deletion after the test run."""

    def _file_fixture_gen_file_repo(**kwargs):
        kwargs.setdefault("name", str(uuid.uuid4()))
        return gen_object_with_cleanup(file_repo_api_client, kwargs)

    yield _file_fixture_gen_file_repo


@pytest.fixture
def gen_bad_response_fixture_server(gen_threaded_aiohttp_server):
    """
    This server will perform 3 bad responses for each file requested.

    1st response will be incomplete, sending only half of the data.
    2nd response will have corrupted data, with one byte changed.
    3rd response will return error 429.
    4th response will be correct.
    """

    def _gen_fixture_server(fixtures_root, ssl_ctx):
        record = []
        num_requests = defaultdict(int)

        async def handler(request):
            nonlocal num_requests
            record.append(request)
            relative_path = request.raw_path[1:]  # Strip off leading "/"
            file_path = Path(fixtures_root) / Path(relative_path)
            # Max retries is 3. So on fourth request, send full data
            num_requests[relative_path] += 1
            if "PULP_MANIFEST" in relative_path or num_requests[relative_path] % 4 == 0:
                return web.FileResponse(file_path)

            # On third request send 429 error, TooManyRequests
            if num_requests[relative_path] % 4 == 3:
                raise web.HTTPTooManyRequests

            size = file_path.stat().st_size
            response = web.StreamResponse(headers={"content-length": f"{size}"})
            await response.prepare(request)
            async with aiofiles.open(file_path, "rb") as f:
                # Send only partial content causing aiohttp.ClientPayloadError if request num == 1
                chunk = await f.read(size // 2)
                await response.write(chunk)
                # Send last chunk with modified last byte if request num == 2
                if num_requests[relative_path] % 4 == 2:
                    chunk2 = await f.read()
                    await response.write(chunk2[:-1])
                    await response.write(bytes([chunk2[-1] ^ 1]))

            await response.write_eof()

        app = web.Application()
        app.add_routes([web.get("/{tail:.*}", handler)])
        return gen_threaded_aiohttp_server(app, ssl_ctx, record)

    yield _gen_fixture_server


@pytest.fixture
def bad_response_fixture_server(file_fixtures_root, gen_bad_response_fixture_server):
    yield gen_bad_response_fixture_server(file_fixtures_root, None)
