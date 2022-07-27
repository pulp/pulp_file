"""Tests related to content path."""
import pytest

from pulp_smash import utils
from pulp_smash.pulp3.utils import gen_distribution
from urllib.parse import urljoin

from .constants import PULP_CONTENT_BASE_URL


@pytest.mark.skip("Skip for pulpcore 3.20")
@pytest.mark.parallel
def test_content_directory_listing(file_distro_api_client, gen_object_with_cleanup):
    """Checks that distributions are grouped by base-path when listing content directories."""
    base_path = utils.uuid4()
    for path in ["/foo1", "/foo2", "/boo/foo1"]:
        gen_object_with_cleanup(
            file_distro_api_client, gen_distribution(base_path=base_path + path)
        )

    response = utils.http_get(PULP_CONTENT_BASE_URL).decode("utf-8")
    assert response.count(f'a href="{base_path}/"') == 1

    url = urljoin(PULP_CONTENT_BASE_URL, base_path + "/")
    response = utils.http_get(url).decode("utf-8")
    assert response.count('a href="foo1/"') == 1
    assert response.count('a href="foo2/"') == 1
    assert response.count('a href="boo/"') == 1

    response = utils.http_get(urljoin(url, "boo/")).decode("utf-8")
    assert response.count('a href="foo1/"') == 1
