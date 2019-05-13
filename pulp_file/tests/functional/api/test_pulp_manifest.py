# coding=utf-8
"""Tests whether Pulp handles PULP_MANIFEST information."""
import csv
import unittest
from functools import reduce
from urllib.parse import urljoin

from pulp_smash import api, config
from pulp_smash.pulp3.constants import (
    REPO_PATH,
)
from pulp_smash.pulp3.utils import (
    gen_distribution,
    gen_repo,
    sync,
)

from pulp_file.tests.functional.constants import (
    FILE_DISTRIBUTION_PATH,
    FILE_FIXTURE_COUNT,
    FILE_REMOTE_PATH,
)
from pulp_file.tests.functional.utils import (
    create_file_publication,
    gen_file_remote,
)
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class AccessingPublishedDataTestCase(unittest.TestCase):
    """Assert that an HTTP error is not raised when accessing published data.

    This test targets the following issue:

    * `Pulp #4519 https://pulp.plan.io/issues/4519`_
    """

    @classmethod
    def setUpClass(cls):
        """Define class-wide variable."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg)

    def test_access_error(self):
        """HTTP error is not raised when accessing published data."""
        repo = self.client.post(REPO_PATH, gen_repo())
        self.addCleanup(self.client.delete, repo['_href'])

        remote = self.client.post(FILE_REMOTE_PATH, gen_file_remote())
        self.addCleanup(self.client.delete, remote['_href'])

        sync(self.cfg, remote, repo)
        repo = self.client.get(repo['_href'])

        publication = create_file_publication(self.cfg, repo)
        self.addCleanup(self.client.delete, publication['_href'])

        body = gen_distribution()
        body['publication'] = publication['_href']

        distribution = self.client.post(FILE_DISTRIBUTION_PATH, body)
        self.addCleanup(self.client.delete, distribution['_href'])

        pulp_manifest = parse_pulp_manifest(
            self.download_pulp_manifest(distribution, 'PULP_MANIFEST')
        )

        self.assertEqual(len(pulp_manifest), FILE_FIXTURE_COUNT, pulp_manifest)

    def download_pulp_manifest(self, distribution, unit_path):
        """Download pulp manifest."""
        unit_url = reduce(
            urljoin,
            (
                self.cfg.get_content_host_base_url(),
                '//' + distribution['base_url'] + '/',
                unit_path,
            ),
        )
        return self.client.using_handler(api.safe_handler).get(unit_url)


def parse_pulp_manifest(pulp_manifest):
    """Parse pulp manifest."""
    return list(csv.DictReader(
        pulp_manifest.text.splitlines(),
        ('name', 'checksum', 'size'),
    ))
