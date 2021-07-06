"""Tests that sync file plugin repositories."""
import unittest

from pulp_smash import config
from pulp_smash.pulp3.bindings import monitor_task, PulpTaskError
from pulp_smash.pulp3.utils import (
    gen_repo,
    get_added_content_summary,
    get_content_summary,
    wget_download_on_host,
)

from pulp_file.tests.functional.constants import (
    FILE_FIXTURE_MANIFEST_URL,
    FILE_FIXTURE_SUMMARY,
    FILE_FIXTURE_URL,
    FILE_INVALID_MANIFEST_URL,
    FILE2_FIXTURE_MANIFEST_URL,
)
from pulp_file.tests.functional.utils import gen_file_client, gen_file_remote
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401

from pulpcore.client.pulp_file import (
    RepositoriesFileApi,
    RepositorySyncURL,
    RemotesFileApi,
    ContentFilesApi,
    PublicationsFileApi,
)


class BasicSyncTestCase(unittest.TestCase):
    """Sync a repository with the file plugin."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = gen_file_client()

    def test_sync_local(self):
        """Test syncing from the local filesystem."""
        wget_download_on_host(FILE_FIXTURE_URL, "/tmp")

        self.do_test("file:///tmp/file/PULP_MANIFEST")

    def test_sync_http(self):
        """Test syncing from the network."""
        self.do_test(FILE_FIXTURE_MANIFEST_URL)

    def do_test(self, url):
        """Sync repositories with the file plugin.

        In order to sync a repository a remote has to be associated within
        this repository. When a repository is created this version field is set
        as None. After a sync the repository version is updated.

        Do the following:

        1. Create a repository, and a remote.
        2. Assert that repository version is None.
        3. Sync the remote.
        4. Assert that repository version is not None.
        5. Assert that the correct number of units were added and are present
           in the repo.
        6. Sync the remote one more time.
        7. Assert that repository version is different from the previous one.
        8. Assert that the same number of are present and that no units were
           added.
        """
        repo_api = RepositoriesFileApi(self.client)
        remote_api = RemotesFileApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        body = gen_file_remote(url)
        remote = remote_api.create(body)
        self.addCleanup(remote_api.delete, remote.pulp_href)

        # Sync the repository.
        self.assertEqual(repo.latest_version_href, f"{repo.pulp_href}versions/0/")
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = repo_api.read(repo.pulp_href)

        self.assertIsNotNone(repo.latest_version_href)
        self.assertDictEqual(get_content_summary(repo.to_dict()), FILE_FIXTURE_SUMMARY)
        self.assertDictEqual(get_added_content_summary(repo.to_dict()), FILE_FIXTURE_SUMMARY)

        # Sync the repository again.
        latest_version_href = repo.latest_version_href
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = repo_api.read(repo.pulp_href)

        self.assertEqual(latest_version_href, repo.latest_version_href)
        self.assertDictEqual(get_content_summary(repo.to_dict()), FILE_FIXTURE_SUMMARY)


class MirrorSyncTestCase(unittest.TestCase):
    """Do a mirrored sync a repository with the file plugin."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = gen_file_client()

        cls.content_api = ContentFilesApi(cls.client)
        cls.repo_api = RepositoriesFileApi(cls.client)
        cls.remote_api = RemotesFileApi(cls.client)
        cls.publications_api = PublicationsFileApi(cls.client)

    def setUp(self):
        """Create remote, repo, and distribution."""
        self.remote = self.remote_api.create(gen_file_remote())
        self.repo = self.repo_api.create(gen_repo())

    def tearDown(self):
        """Clean up."""
        monitor_task(self.repo_api.delete(self.repo.pulp_href).task)
        monitor_task(self.remote_api.delete(self.remote.pulp_href).task)

    def test_01_sync(self):
        """Assert that syncing the repository w/ mirror=True creates a publication."""
        # Sync the repository.
        repository_sync_data = RepositorySyncURL(remote=self.remote.pulp_href, mirror=True)
        sync_response = self.repo_api.sync(self.repo.pulp_href, repository_sync_data)
        task = monitor_task(sync_response.task)

        # Check that all the appropriate resources were created
        self.assertEqual(len(task.created_resources), 2)
        self.assertTrue(any(["publication" in resource for resource in task.created_resources]))
        self.assertTrue(any(["version" in resource for resource in task.created_resources]))


class SyncInvalidTestCase(unittest.TestCase):
    """Sync a repository with a given url on the remote."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.client = gen_file_client()

    def test_invalid_url(self):
        """Sync a repository using a remote url that does not exist.

        Test that we get a task failure. See :meth:`do_test`.
        """
        with self.assertRaises(PulpTaskError) as cm:
            task = self.do_test("http://i-am-an-invalid-url.com/invalid/")
        task = cm.exception.task.to_dict()
        self.assertIsNotNone(task["error"]["description"])

    def test_invalid_file(self):
        """Sync a repository using an invalid file repository.

        Assert that an exception is raised, and that error message has
        keywords related to the reason of the failure. See :meth:`do_test`.
        """
        with self.assertRaises(PulpTaskError) as cm:
            task = self.do_test(FILE_INVALID_MANIFEST_URL)
        task = cm.exception.task.to_dict()
        for key in ("checksum", "failed"):
            self.assertIn(key, task["error"]["description"])

    def do_test(self, url):
        """Sync a repository given ``url`` on the remote."""
        repo_api = RepositoriesFileApi(self.client)
        remote_api = RemotesFileApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        body = gen_file_remote(url=url)
        remote = remote_api.create(body)
        self.addCleanup(remote_api.delete, remote.pulp_href)

        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        return monitor_task(sync_response.task)


class SyncDuplicateFileRepoTestCase(unittest.TestCase):
    """Sync multiple remotes containing duplicate files."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.client = gen_file_client()

    def test_duplicate_file_sync(self):
        """Sync a repository with remotes containing same file names.

        This test does the following.

        1. Create a repository in pulp.
        2. Create two remotes containing the same file.
        3. Check whether the created repo has only one copy of the file.

        This test targets the following issue:

        `Pulp #4738 <https://pulp.plan.io/issues/4738>`_
        """
        repo_api = RepositoriesFileApi(self.client)
        remote_api = RemotesFileApi(self.client)

        # Step 1
        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        # Step 2
        remote = remote_api.create(gen_file_remote())
        self.addCleanup(remote_api.delete, remote.pulp_href)
        remote2 = remote_api.create(gen_file_remote(url=FILE2_FIXTURE_MANIFEST_URL))

        self.addCleanup(remote_api.delete, remote2.pulp_href)
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = repo_api.read(repo.pulp_href)
        self.assertDictEqual(get_content_summary(repo.to_dict()), FILE_FIXTURE_SUMMARY)
        self.assertDictEqual(get_added_content_summary(repo.to_dict()), FILE_FIXTURE_SUMMARY)

        repository_sync_data = RepositorySyncURL(remote=remote2.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = repo_api.read(repo.pulp_href)
        self.assertDictEqual(get_added_content_summary(repo.to_dict()), FILE_FIXTURE_SUMMARY)
