"""Tests that look at generic list endpoints."""
import uuid

import pytest

from pulpcore.client.pulp_certguard import (
    ApiClient as CertGuardApiClient,
    ContentguardsX509Api,
)


@pytest.mark.parallel
def test_read_all_repos_generic(file_repo_api_client, file_repo):
    """Ensure name is displayed when listing repositories generic."""
    response = file_repo_api_client.list()
    assert response.count != 0
    for repo in response.results:
        assert repo.name is not None


@pytest.mark.parallel
def test_read_all_content_generic(file_content_api_client, file_random_content_unit):
    """Ensure href is displayed when listing content generic."""
    response = file_content_api_client.list()
    assert response.count != 0
    for content in response.results:
        assert content.pulp_href is not None


@pytest.mark.parallel
def test_read_all_content_guards_generic(
    content_guards_api_client, tls_certificate_authority_cert, bindings_cfg
):
    """Ensure name is displayed when listing content guards generic."""
    cert_guards_api = ContentguardsX509Api(CertGuardApiClient(bindings_cfg))
    cert_guards_api.create(
        {"name": str(uuid.uuid4()), "ca_certificate": tls_certificate_authority_cert}
    )

    response = content_guards_api_client.list()
    assert response.count != 0
    for content_guard in response.results:
        assert content_guard.name is not None
