"""Tests related to content path."""
import pytest
import uuid

from pulp_smash import utils
from pulp_smash.pulp3.utils import gen_distribution
from urllib.parse import urljoin

from pulpcore.app import settings
from pulp_file.tests.functional.utils import get_url
from .constants import PULP_CONTENT_BASE_URL


@pytest.mark.parallel
def test_content_directory_listing(
    file_distro_api_client,
    gen_object_with_cleanup,
    tls_certificate_authority_cert,
    x509_content_guards_api_client,
):
    """Checks that distributions are grouped by base-path when listing content directories."""

    HIDE_GUARDED_DISTRIBUTIONS = getattr(settings, "HIDE_GUARDED_DISTRIBUTIONS", False)

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

    response = utils.http_get(PULP_CONTENT_BASE_URL).decode("utf-8")
    assert response.count(f'a href="{base_path}/"') == 1

    url = urljoin(PULP_CONTENT_BASE_URL, base_path + "/")
    response = utils.http_get(url).decode("utf-8")
    assert response.count('a href="foo1/"') == 1
    assert response.count('a href="foo2/"') == (0 if HIDE_GUARDED_DISTRIBUTIONS else 1)
    assert response.count('a href="boo1/"') == 1
    assert response.count('a href="boo2/"') == (0 if HIDE_GUARDED_DISTRIBUTIONS else 1)

    response = utils.http_get(urljoin(url, "boo1/")).decode("utf-8")
    assert response.count('a href="foo1/"') == 1

    # Assert that not using a trailing slash on the root returns a 301
    response = get_url(PULP_CONTENT_BASE_URL[:-1])
    assert response.history[0].status == 301
    assert response.status == 200

    # Assert that not using a trailing slash returns a 301 for a partial base path
    url = urljoin(PULP_CONTENT_BASE_URL, base_path)
    response = get_url(url)
    assert response.history[0].status == 301
    assert response.status == 200

    # Assert that not using a trailing slash within a distribution returns a 301
    url = f"{url}/boo1"
    response = get_url(url)
    assert response.history[0].status == 301
    assert response.status == 200

    # Assert that not using a trailing slash for a full base path returns a 301
    url = f"{url}/foo1"
    response = get_url(url)
    assert response.history[0].status == 301
    assert response.status == 404
    assert "Distribution is not pointing to" in response.reason

    # Assert that a non-existing base path does not return a 301
    url = url[:-1]
    response = get_url(url)
    assert len(response.history) == 0
    assert response.status == 404
