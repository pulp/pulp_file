# coding=utf-8
"""Tests that sync file plugin repositories."""
import unittest

from pulp_smash import config
from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import gen_repo, download_content_unit

from pulp_file.tests.functional.utils import gen_file_client, gen_file_remote
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401

from pulpcore.client.pulp_file import (
    ContentFilesApi,
    DistributionsFileApi,
    PublicationsFileApi,
    RepositoriesFileApi,
    RepositorySyncURL,
    RemotesFileApi,
)


class AutoPublishDistributeTestCase(unittest.TestCase):
    """Test auto-publish and auto-distribution"""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = gen_file_client()

        cls.content_api = ContentFilesApi(cls.client)
        cls.repo_api = RepositoriesFileApi(cls.client)
        cls.remote_api = RemotesFileApi(cls.client)
        cls.publications_api = PublicationsFileApi(cls.client)
        cls.distributions_api = DistributionsFileApi(cls.client)

        cls.CUSTOM_MANIFEST = "TEST_MANIFEST"

    def setUp(self):
        """Create remote, repo, and distribution."""
        self.remote = self.remote_api.create(gen_file_remote())
        self.repo = self.repo_api.create(gen_repo(manifest=self.CUSTOM_MANIFEST, autopublish=True))
        response = self.distributions_api.create(
            {"name": "foo", "base_path": "bar/foo", "repository": self.repo.pulp_href}
        )
        distribution_href = monitor_task(response.task).created_resources[0]
        self.distribution = self.distributions_api.read(distribution_href)

    def tearDown(self):
        """Clean up."""
        monitor_task(self.repo_api.delete(self.repo.pulp_href).task)
        monitor_task(self.remote_api.delete(self.remote.pulp_href).task)
        monitor_task(self.distributions_api.delete(self.distribution.pulp_href).task)

    def test_01_sync(self):
        """Assert that syncing the repository triggers auto-publish and auto-distribution."""
        self.assertEqual(self.publications_api.list().count, 0)
        self.assertTrue(self.distribution.publication is None)

        # Sync the repository.
        repository_sync_data = RepositorySyncURL(remote=self.remote.pulp_href)
        sync_response = self.repo_api.sync(self.repo.pulp_href, repository_sync_data)
        task = monitor_task(sync_response.task)

        # Check that all the appropriate resources were created
        self.assertGreater(len(task.created_resources), 1)
        publications = self.publications_api.list()
        self.assertEqual(publications.count, 1)
        download_content_unit(self.cfg, self.distribution.to_dict(), self.CUSTOM_MANIFEST)

        # Check that the publish settings were used
        publication = publications.results[0]
        self.assertEqual(publication.manifest, self.CUSTOM_MANIFEST)

        # Sync the repository again. Since there should be no new repository version, there
        # should be no new publications or distributions either.
        sync_response = self.repo_api.sync(self.repo.pulp_href, repository_sync_data)
        task = monitor_task(sync_response.task)

        self.assertEqual(len(task.created_resources), 0)
        self.assertEqual(self.publications_api.list().count, 1)

    def test_02_modify(self):
        """Assert that modifying the repository triggers auto-publish and auto-distribution."""
        self.assertEqual(self.publications_api.list().count, 0)
        self.assertTrue(self.distribution.publication is None)

        # Modify the repository by adding a coment unit
        content = self.content_api.list().results[0].pulp_href
        modify_response = self.repo_api.modify(
            self.repo.pulp_href, {"add_content_units": [content]}
        )
        task = monitor_task(modify_response.task)

        # Check that all the appropriate resources were created
        self.assertGreater(len(task.created_resources), 1)
        publications = self.publications_api.list()
        self.assertEqual(publications.count, 1)

        # Check that the publish settings were used
        publication = publications.results[0]
        self.assertEqual(publication.manifest, self.CUSTOM_MANIFEST)
