# coding=utf-8
"""Tests that sync file plugin repositories."""
import unittest

from pulp_smash import api, cli, config
from pulp_smash.exceptions import TaskReportError
from pulp_smash.pulp3.constants import MEDIA_PATH, REPO_PATH
from pulp_smash.pulp3.utils import (
    gen_repo,
    get_added_content_summary,
    get_content_summary,
    sync,
)

from pulp_file.tests.functional.constants import (
    FILE2_FIXTURE_MANIFEST_URL,
    FILE_FIXTURE_SUMMARY,
    FILE_INVALID_MANIFEST_URL,
    FILE_REMOTE_PATH,
)
from pulp_file.tests.functional.utils import gen_file_remote
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class BasicFileSyncTestCase(unittest.TestCase):
    """Sync a repository with the file plugin."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)

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
        repo = self.client.post(REPO_PATH, gen_repo())
        self.addCleanup(self.client.delete, repo['_href'])

        body = gen_file_remote()
        remote = self.client.post(FILE_REMOTE_PATH, body)
        self.addCleanup(self.client.delete, remote['_href'])

        # Sync the repository.
        self.assertIsNone(repo['_latest_version_href'])
        sync(self.cfg, remote, repo)
        repo = self.client.get(repo['_href'])

        self.assertIsNotNone(repo['_latest_version_href'])
        self.assertDictEqual(get_content_summary(repo), FILE_FIXTURE_SUMMARY)
        self.assertDictEqual(get_added_content_summary(repo), FILE_FIXTURE_SUMMARY)

        # Sync the repository again.
        latest_version_href = repo['_latest_version_href']
        sync(self.cfg, remote, repo)
        repo = self.client.get(repo['_href'])

        self.assertNotEqual(latest_version_href, repo['_latest_version_href'])
        self.assertDictEqual(get_content_summary(repo), FILE_FIXTURE_SUMMARY)
        self.assertDictEqual(get_added_content_summary(repo), {})

    def test_file_decriptors(self):
        """Test whether file descriptors are closed properly.

        This test targets the following issue:

        `Pulp #4073 <https://pulp.plan.io/issues/4073>`_

        Do the following:

        1. Check if 'lsof' is installed. If it is not, skip this test.
        2. Create and sync a repo.
        3. Run the 'lsof' command to verify that files in the
           path ``/var/lib/pulp/`` are closed after the sync.
        4. Assert that issued command returns `0` opened files.
        """
        cli_client = cli.Client(self.cfg, cli.echo_handler)

        # check if 'lsof' is available
        if cli_client.run(('which', 'lsof')).returncode != 0:
            raise unittest.SkipTest('lsof package is not present')

        repo = self.client.post(REPO_PATH, gen_repo())
        self.addCleanup(self.client.delete, repo['_href'])

        remote = self.client.post(FILE_REMOTE_PATH, gen_file_remote())
        self.addCleanup(self.client.delete, remote['_href'])

        sync(self.cfg, remote, repo)

        cmd = 'lsof -t +D {}'.format(MEDIA_PATH).split()
        response = cli_client.run(cmd).stdout
        self.assertEqual(len(response), 0, response)


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


class SyncDuplicateFileRepoTestCase(unittest.TestCase):
    """Sync multiple remotes containing duplicate files."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)

    def test_duplicate_file_sync(self):
        """Sync a repository with remotes containing same file names.

        This test does the following.

        1. Create a repository in pulp.
        2. Create two remotes containing the same file.
        3. Check whether the created repo has only one copy of the file.

        This test targets the following issue:

        `Pulp #4738 <https://pulp.plan.io/issues/4738>`_
        """
        # Step 1
        repo = self.client.post(REPO_PATH, gen_repo())
        self.addCleanup(self.client.delete, repo['_href'])

        # Step 2
        remote = self.client.post(
            FILE_REMOTE_PATH,
            gen_file_remote()
        )
        self.addCleanup(self.client.delete, remote['_href'])
        remote2 = self.client.post(
            FILE_REMOTE_PATH,
            gen_file_remote(url=FILE2_FIXTURE_MANIFEST_URL)
        )
        self.addCleanup(self.client.delete, remote2['_href'])
        sync(self.cfg, remote, repo)
        repo = self.client.get(repo['_href'])
        self.assertDictEqual(get_content_summary(repo), FILE_FIXTURE_SUMMARY)
        self.assertDictEqual(get_added_content_summary(repo), FILE_FIXTURE_SUMMARY)

        sync(self.cfg, remote2, repo)
        repo = self.client.get(repo['_href'])
        self.assertDictEqual(get_added_content_summary(repo), FILE_FIXTURE_SUMMARY)
