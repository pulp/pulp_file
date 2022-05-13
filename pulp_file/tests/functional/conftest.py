import logging
import tempfile
import uuid

from pathlib import Path

import pytest

from pulpcore.client.pulp_file import (
    ApiClient,
    AcsFileApi,
    ContentFilesApi,
    DistributionsFileApi,
    FileFileAlternateContentSource,
    RepositoriesFileApi,
    RepositoriesFileVersionsApi,
    RemotesFileApi,
    PublicationsFileApi,
)

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import gen_repo

from pulp_file.tests.functional.utils import gen_file_client, generate_iso, generate_manifest


_logger = logging.getLogger(__name__)


def pytest_check_for_leftover_pulp_objects(config):
    file_client = gen_file_client()

    types_to_check = [
        FileFileAlternateContentSource(file_client),
        RemotesFileApi(file_client),
    ]
    for type_to_check in types_to_check:
        if type_to_check.list().count > 0:
            raise Exception(f"This test left over a {type_to_check}.")


@pytest.fixture
def file_client(cid, bindings_cfg):
    api_client = ApiClient(bindings_cfg)
    api_client.default_headers["Correlation-ID"] = cid
    return api_client


@pytest.fixture
def file_acs_api_client(file_client):
    return AcsFileApi(file_client)


@pytest.fixture
def file_content_api_client(file_client):
    return ContentFilesApi(file_client)


@pytest.fixture
def file_random_content_unit(file_content_api_client, tmp_path):
    with tempfile.NamedTemporaryFile(dir=tmp_path) as tmp_file:
        tmp_file.write(b"not empty")
        tmp_file.flush()
        return monitor_task(
            file_content_api_client.create(relative_path=str(uuid.uuid4()), file=tmp_file.name).task
        )


@pytest.fixture
def file_distro_api_client(file_client):
    return DistributionsFileApi(file_client)


@pytest.fixture
def file_pub_api_client(file_client):
    return PublicationsFileApi(file_client)


@pytest.fixture
def file_repo_api_client(file_client):
    return RepositoriesFileApi(file_client)


@pytest.fixture
def file_repo_ver_api_client(file_client):
    return RepositoriesFileVersionsApi(file_client)


@pytest.fixture
def file_repo(file_repo_api_client, gen_object_with_cleanup):
    return gen_object_with_cleanup(file_repo_api_client, gen_repo())


@pytest.fixture
def file_remote_api_client(file_client):
    return RemotesFileApi(file_client)


@pytest.fixture
def file_fixtures_root(tmpdir):
    return Path(tmpdir)


@pytest.fixture
def basic_manifest_path(file_fixtures_root):
    file_fixtures_root.joinpath("basic").mkdir()
    file1 = generate_iso(file_fixtures_root.joinpath("basic/1.iso"))
    file2 = generate_iso(file_fixtures_root.joinpath("basic/2.iso"))
    file3 = generate_iso(file_fixtures_root.joinpath("basic/3.iso"))
    generate_manifest(file_fixtures_root.joinpath("basic/PULP_MANIFEST"), [file1, file2, file3])
    return "/basic/PULP_MANIFEST"


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
        return gen_object_with_cleanup(file_repo_api_client, kwargs)

    yield _file_fixture_gen_file_repo
