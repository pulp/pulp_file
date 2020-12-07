# coding=utf-8
"""Tests whether Pulp handles PULP_MANIFEST information."""
import csv
import requests
import unittest
from urllib.parse import urljoin

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import gen_distribution, gen_repo

from pulp_file.tests.functional.constants import FILE_FIXTURE_COUNT
from pulp_file.tests.functional.utils import gen_file_client, gen_file_remote
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401

from pulpcore.client.pulp_file import (
    DistributionsFileApi,
    PublicationsFileApi,
    RepositoriesFileApi,
    RepositorySyncURL,
    RemotesFileApi,
    FileFilePublication,
)


class AccessingPublishedDataTestCase(unittest.TestCase):
    """Assert that an HTTP error is not raised when accessing published data.

    This test targets the following issue:

    * `Pulp #4519 https://pulp.plan.io/issues/4519`_
    """

    @classmethod
    def setUpClass(cls):
        """Define class-wide variable."""
        cls.client = gen_file_client()

    def test_access_error(self):
        """HTTP error is not raised when accessing published data."""
        repo_api = RepositoriesFileApi(self.client)
        remote_api = RemotesFileApi(self.client)
        publications = PublicationsFileApi(self.client)
        distributions = DistributionsFileApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        remote = remote_api.create(gen_file_remote())
        self.addCleanup(remote_api.delete, remote.pulp_href)

        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = repo_api.read(repo.pulp_href)

        publish_data = FileFilePublication(repository=repo.pulp_href)
        publish_response = publications.create(publish_data)
        created_resources = monitor_task(publish_response.task).created_resources
        publication_href = created_resources[0]
        self.addCleanup(publications.delete, publication_href)

        body = gen_distribution()
        body["publication"] = publication_href

        distribution_response = distributions.create(body)
        created_resources = monitor_task(distribution_response.task).created_resources
        distribution = distributions.read(created_resources[0])
        self.addCleanup(distributions.delete, distribution.pulp_href)

        pulp_manifest = parse_pulp_manifest(
            self.download_pulp_manifest(distribution.to_dict(), "PULP_MANIFEST")
        )

        self.assertEqual(len(pulp_manifest), FILE_FIXTURE_COUNT, pulp_manifest)

    def download_pulp_manifest(self, distribution, unit_path):
        """Download pulp manifest."""
        unit_url = urljoin(distribution["base_url"] + "/", unit_path)
        return requests.get(unit_url)


def parse_pulp_manifest(pulp_manifest):
    """Parse pulp manifest."""
    return list(csv.DictReader(pulp_manifest.text.splitlines(), ("name", "checksum", "size")))
