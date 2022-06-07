"""Tests related to content path."""
import pytest
import unittest

from pulp_smash import api, config, utils
from pulp_smash.pulp3.bindings import delete_orphans
from pulp_smash.pulp3.utils import gen_remote, gen_repo, sync, gen_distribution
from urllib.parse import urljoin

from pulp_file.tests.functional.utils import create_file_publication
from .constants import (
    FILE_FIXTURE_MANIFEST_URL,
    FILE_REMOTE_PATH,
    FILE_REPO_PATH,
    PULP_CONTENT_BASE_URL,
)


class SyncPublishContentPathTestCase(unittest.TestCase):
    """Test whether sync/publish for content already in Pulp.

    Different code paths are used in Pulp for the cases when artifacts are
    already present on the filesystem during sync and when they are not
    downloaded yet

    This test targets the following issue:

    `Pulp #4442 <https://pulp.plan.io/issues/4442>`_

    Does the following:

    1. Assure that no content from repository A is downloaded.
    2. Sync/publish repository A with download policy immediate.
    3. Sync/publish repository A again with download policy immediate.
    4. No failure in 2 shows that sync went fine when content was
       not present on the disk and in the database.
    5. No failure in 3 shows that sync went fine when content was already
       present on the disk and in the database.

    """

    def test_all(self):
        """Test whether sync/publish for content already in Pulp."""
        cfg = config.get_config()
        client = api.Client(cfg, api.page_handler)

        # step 1. delete orphans to assure that no content is present on disk,
        # or database.
        delete_orphans()

        remote = client.post(FILE_REMOTE_PATH, gen_remote(FILE_FIXTURE_MANIFEST_URL))
        self.addCleanup(client.delete, remote["pulp_href"])

        repo = client.post(FILE_REPO_PATH, gen_repo())
        self.addCleanup(client.delete, repo["pulp_href"])

        for _ in range(2):
            sync(cfg, remote, repo)
            repo = client.get(repo["pulp_href"])
            create_file_publication(cfg, repo)


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
