import hashlib
import unittest
from random import choice
from urllib.parse import urljoin

from pulp_smash import config, utils
from pulp_smash.pulp3.bindings import (
    PulpTaskError,
    delete_orphans,
    monitor_task,
    monitor_task_group,
)
from pulp_smash.pulp3.utils import download_content_unit, gen_distribution
from pulpcore.client.pulp_file import (
    AcsFileApi,
    DistributionsFileApi,
    PublicationsFileApi,
    RemotesFileApi,
    RepositoriesFileApi,
    RepositorySyncURL,
)
from pulpcore.client.pulp_file.exceptions import ApiException
from pulpcore.tests.functional.api.using_plugin.utils import (
    gen_file_client,
    gen_file_remote,
    gen_repo,
)

from pulp_file.tests.functional.constants import (
    FILE_FIXTURE_MANIFEST_URL,
    FILE_FIXTURE_URL,
    FILE_MANIFEST_ONLY_FIXTURE_URL,
    PULP_FIXTURES_BASE_URL,
)
from pulp_file.tests.functional.utils import get_file_content_paths


class AlternateContentSourceTestCase(unittest.TestCase):
    """Test File ACS."""

    @classmethod
    def setUpClass(cls):
        """
        Create class-wide variables.

        Variables 'paths' and 'paths_updated' are defined as strings.
        In same way data are send from user.
        """
        cls.cfg = config.get_config()
        cls.file_client = gen_file_client()
        cls.repo_api = RepositoriesFileApi(cls.file_client)
        cls.file_remote_api = RemotesFileApi(cls.file_client)
        cls.file_acs_api = AcsFileApi(cls.file_client)
        cls.publication_api = PublicationsFileApi(cls.file_client)
        cls.distribution_api = DistributionsFileApi(cls.file_client)
        cls.paths = ["goodpath/PULP_MANIFEST", "test", "whatever/test"]

    @classmethod
    def tearDownClass(cls):
        """Run orphan cleanup."""
        delete_orphans()

    def _create_acs(self, name="file_acs", paths=None, remote_url=FILE_FIXTURE_MANIFEST_URL):
        remote = self.file_remote_api.create(gen_file_remote(remote_url, policy="on_demand"))
        self.addCleanup(self.file_remote_api.delete, remote.pulp_href)

        acs_data = {
            "name": name,
            "remote": remote.pulp_href,
        }
        if paths:
            acs_data["paths"] = paths

        acs = self.file_acs_api.create(acs_data)
        self.addCleanup(self.file_acs_api.delete, acs.pulp_href)

        return acs

    def test_path_validation(self):
        """Test the validation of paths."""
        # path is wrong, begins with /
        with self.assertRaises(ApiException) as ctx:
            self._create_acs(paths=(self.paths + ["/bad_path"]))
        self.assertEqual(ctx.exception.status, 400)

        # use valid paths
        acs = self._create_acs(paths=self.paths)
        self.assertEqual(sorted(acs.paths), sorted(self.paths))

    def test_acs_sync(self):
        """Test syncing from an ACS."""
        repo = self.repo_api.create(gen_repo())
        self.addCleanup(self.repo_api.delete, repo.pulp_href)

        remote = self.file_remote_api.create(gen_file_remote(FILE_MANIFEST_ONLY_FIXTURE_URL))
        self.addCleanup(self.file_remote_api.delete, remote.pulp_href)

        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)

        # sync should fail as the repo has metadata only (no files)
        sync_response = self.repo_api.sync(repo.pulp_href, repository_sync_data)
        with self.assertRaises(PulpTaskError) as ctx:
            monitor_task(sync_response.task)
        self.assertIn("404", ctx.exception.task.error["description"])

        # create an acs and pull in its remote artifacts
        acs = self._create_acs()
        resp = self.file_acs_api.refresh(acs.pulp_href, acs)
        monitor_task_group(resp.task_group)

        # the sync should now work as the files are being pulled from ACS remote
        sync_response = self.repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)

    def test_acs_sync_with_paths(self):
        """Test syncing from an ACS using different paths."""
        repo = self.repo_api.create(gen_repo())
        self.addCleanup(self.repo_api.delete, repo.pulp_href)

        remote = self.file_remote_api.create(gen_file_remote(FILE_MANIFEST_ONLY_FIXTURE_URL))
        self.addCleanup(self.file_remote_api.delete, remote.pulp_href)

        acs = self._create_acs(
            paths=("file/PULP_MANIFEST", "file2/PULP_MANIFEST"),
            remote_url=PULP_FIXTURES_BASE_URL,
        )
        resp = self.file_acs_api.refresh(acs.pulp_href, acs)
        task_group = monitor_task_group(resp.task_group)
        self.assertEquals(len(task_group.tasks), 2)

        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = self.repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)

    def test_serving_acs_content(self):
        """Test serving of ACS content through the content app."""
        cfg = config.get_config()
        acs = self._create_acs()
        resp = self.file_acs_api.refresh(acs.pulp_href, acs)
        monitor_task_group(resp.task_group)

        remote = self.file_remote_api.create(
            gen_file_remote(FILE_MANIFEST_ONLY_FIXTURE_URL, policy="on_demand")
        )
        self.addCleanup(self.file_remote_api.delete, remote.pulp_href)

        repo = self.repo_api.create(gen_repo(remote=remote.pulp_href, autopublish=True))
        self.addCleanup(self.repo_api.delete, repo.pulp_href)

        distribution_response = self.distribution_api.create(
            gen_distribution(repository=repo.pulp_href)
        )
        created_resources = monitor_task(distribution_response.task).created_resources
        distribution = self.distribution_api.read(created_resources[0])
        self.addCleanup(self.distribution_api.delete, distribution.pulp_href)

        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = self.repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = self.repo_api.read(repo.pulp_href)

        unit_path = choice(get_file_content_paths(repo.to_dict()))
        fixtures_hash = hashlib.sha256(
            utils.http_get(urljoin(FILE_FIXTURE_URL, unit_path))
        ).hexdigest()
        content = download_content_unit(cfg, distribution.to_dict(), unit_path)
        pulp_hash = hashlib.sha256(content).hexdigest()

        self.assertEqual(fixtures_hash, pulp_hash)
