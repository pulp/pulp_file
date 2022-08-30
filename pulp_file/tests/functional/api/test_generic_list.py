"""Tests that look at generic list endpoints."""
import uuid

import pytest


@pytest.mark.parallel
def test_read_all_repos_generic(repositories_api_client, file_repo):
    """Ensure name is displayed when listing repositories generic."""
    response = repositories_api_client.list()
    assert response.count != 0
    for repo in response.results:
        assert repo.name is not None


@pytest.mark.parallel
def test_read_all_content_generic(content_api_client, file_random_content_unit):
    """Ensure href is displayed when listing content generic."""
    response = content_api_client.list()
    assert response.count != 0
    for content in response.results:
        assert content.pulp_href is not None


@pytest.mark.parallel
def test_read_all_content_guards_generic(
    gen_object_with_cleanup,
    content_guards_api_client,
    tls_certificate_authority_cert,
    x509_content_guards_api_client,
):
    """Ensure name is displayed when listing content guards generic."""
    gen_object_with_cleanup(
        x509_content_guards_api_client,
        {"name": str(uuid.uuid4()), "ca_certificate": tls_certificate_authority_cert},
    )

    response = content_guards_api_client.list()
    assert response.count != 0
    for content_guard in response.results:
        assert content_guard.name is not None
