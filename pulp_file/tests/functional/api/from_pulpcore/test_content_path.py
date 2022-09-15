"""Tests related to content path."""
import pytest
import uuid

from pulp_smash import utils
from pulp_smash.pulp3.utils import gen_distribution
from urllib.parse import urljoin

from .constants import PULP_CONTENT_BASE_URL


@pytest.mark.parallel
def test_content_directory_listing(
    file_distro_api_client,
    gen_object_with_cleanup,
    tls_certificate_authority_cert,
    x509_content_guards_api_client,
    pulp_settings,
):
    """Checks that distributions are grouped by base-path when listing content directories."""

    HIDE_GUARDED_DISTRIBUTIONS = getattr(pulp_settings, "HIDE_GUARDED_DISTRIBUTIONS", False)

    content_guard1 = gen_object_with_cleanup(
        x509_content_guards_api_client,
        {"name": str(uuid.uuid4()), "ca_certificate": tls_certificate_authority_cert},
    )

    base_path = str(uuid.uuid4())
    for path, content_guard in [
        ("/foo1", None),
        ("/foo2", content_guard1.pulp_href),
        ("/boo1/foo1", None),
        ("/boo2/foo1", content_guard1.pulp_href),
    ]:
        gen_object_with_cleanup(
            file_distro_api_client,
            gen_distribution(base_path=base_path + path, content_guard=content_guard),
        )

    base_url = PULP_CONTENT_BASE_URL
    if pulp_settings.DOMAIN_ENABLED:
        base_url = urljoin(base_url, "default/")
    response = utils.http_get(base_url).decode("utf-8")
    assert response.count(f'a href="{base_path}/"') == 1
    assert response.count('a href="../"') == 0

    url = urljoin(base_url, base_path + "/")
    response = utils.http_get(url).decode("utf-8")
    assert response.count('a href="foo1/"') == 1
    assert response.count('a href="foo2/"') == (0 if HIDE_GUARDED_DISTRIBUTIONS else 1)
    assert response.count('a href="boo1/"') == 1
    assert response.count('a href="boo2/"') == (0 if HIDE_GUARDED_DISTRIBUTIONS else 1)
    assert response.count('a href="../"') == 1

    response = utils.http_get(urljoin(url, "boo1/")).decode("utf-8")
    assert response.count('a href="foo1/"') == 1
