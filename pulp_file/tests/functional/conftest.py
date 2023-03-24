import pytest
from packaging.version import parse as parse_version

from pulpcore.client.pulp_file import (
    FileFileAlternateContentSource,
)
from pulp_file.tests.functional import (
    file_repository_api_client,
    file_repository_version_api_client,
    file_publication_api_client,
    file_distribution_api_client,
    file_remote_factory,
    file_remote_ssl_factory,
    file_remote_client_cert_req_factory,
    file_repository_factory,
)
from pulp_file.tests.functional.utils import gen_file_client

# Aliases for fixtures to go away...
file_repo_api_client = file_repository_api_client
file_repo_ver_api_client = file_repository_version_api_client
file_pub_api_client = file_publication_api_client
file_distro_api_client = file_distribution_api_client
file_fixture_gen_remote = file_remote_factory
file_fixture_gen_remote_ssl = file_remote_ssl_factory
file_fixture_gen_remote_client_cert_req = file_remote_client_cert_req_factory
file_fixture_gen_file_repo = file_repository_factory


def pytest_check_for_leftover_pulp_objects(config):
    file_client = gen_file_client()

    types_to_check = [FileFileAlternateContentSource(file_client)]
    for type_to_check in types_to_check:
        if type_to_check.list().count > 0:
            raise Exception(f"This test left over a {type_to_check}.")


# ----8<--------8<--------8<--------8<--------8<----
# Remove these once they are available in pulpcore


@pytest.fixture(scope="session")
def pulp_versions(status_api_client):
    status = status_api_client.status_read()
    return {item.component: parse_version(item.version) for item in status.versions}


@pytest.fixture
def needs_pulp_plugin(pulp_versions):
    """Skip test if a component is not available in the specified version range"""

    def _needs_pulp_plugin(plugin, min=None, max=None):
        if plugin not in pulp_versions:
            pytest.skip(f"Plugin {plugin} is not installed.")
        if min is not None and pulp_versions[plugin] < parse_version(min):
            pytest.skip(f"Plugin {plugin} too old (<{min}).")
        if max is not None and pulp_versions[plugin] >= parse_version(max):
            pytest.skip(f"Plugin {plugin} too new (>={max}).")

    return _needs_pulp_plugin


@pytest.fixture
def has_pulp_plugin(pulp_versions):
    def _has_pulp_plugin(plugin, min=None, max=None):
        if plugin not in pulp_versions:
            return False
        if min is not None and pulp_versions[plugin] < parse_version(min):
            return False
        if max is not None and pulp_versions[plugin] >= parse_version(max):
            return False
        return True

    return _has_pulp_plugin


# ----8<--------8<--------8<--------8<--------8<----
