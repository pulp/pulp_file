# coding=utf-8
"""Tests that sync file plugin repositories."""
import unittest

from pulp_smash import api, config
from pulp_smash.exceptions import TaskReportError
from pulp_smash.pulp3.constants import REPO_PATH
from pulp_smash.pulp3.utils import (
    gen_repo,
    get_added_content,
    get_content,
    sync,
)

from pulp_file.tests.functional.constants import (
    FILE_FIXTURE_COUNT,
    FILE_INVALID_MANIFEST_URL,
    FILE_REMOTE_PATH
)
from pulp_file.tests.functional.utils import gen_file_remote
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class BasicFileSyncTestCase(unittest.TestCase):
    """Sync a repository with the file plugin."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()

    def test_sync(self):
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
        client = api.Client(self.cfg, api.json_handler)

        repo = client.post(REPO_PATH, gen_repo())
        self.addCleanup(client.delete, repo['_href'])

        body = gen_file_remote()
        remote = client.post(FILE_REMOTE_PATH, body)
        self.addCleanup(client.delete, remote['_href'])

        # Sync the repository.
        self.assertIsNone(repo['_latest_version_href'])
        sync(self.cfg, remote, repo)
        repo = client.get(repo['_href'])

        self.assertIsNotNone(repo['_latest_version_href'])
        self.assertEqual(len(get_content(repo)), FILE_FIXTURE_COUNT)
        self.assertEqual(len(get_added_content(repo)), FILE_FIXTURE_COUNT)

        # Sync the repository again.
        latest_version_href = repo['_latest_version_href']
        sync(self.cfg, remote, repo)
        repo = client.get(repo['_href'])

        self.assertNotEqual(latest_version_href, repo['_latest_version_href'])
        self.assertEqual(len(get_content(repo)), FILE_FIXTURE_COUNT)
        self.assertEqual(len(get_added_content(repo)), 0)


class SyncInvalidTestCase(unittest.TestCase):
    """Sync a repository with a given url on the remote."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)

    def test_invalid_url(self):
        """Sync a repository using a remote url that does not exist.

        Test that we get a task failure. See :meth:`do_test`.
        """
        context = self.do_test('http://i-am-an-invalid-url.com/invalid/')
        self.assertIsNotNone(context.exception.task['error']['description'])

    def test_invalid_file(self):
        """Sync a repository using an invalid file repository.

        Assert that an exception is raised, and that error message has
        keywords related to the reason of the failure. See :meth:`do_test`.
        """
        context = self.do_test(FILE_INVALID_MANIFEST_URL)
        for key in ('checksum', 'failed'):
            self.assertIn(key, context.exception.task['error']['description'])

    def do_test(self, url):
        """Sync a repository given ``url`` on the remote."""
        repo = self.client.post(REPO_PATH, gen_repo())
        self.addCleanup(self.client.delete, repo['_href'])
        body = gen_file_remote(url=url)
        remote = self.client.post(FILE_REMOTE_PATH, body)
        self.addCleanup(self.client.delete, remote['_href'])
        with self.assertRaises(TaskReportError) as context:
            sync(self.cfg, remote, repo)
        return context
