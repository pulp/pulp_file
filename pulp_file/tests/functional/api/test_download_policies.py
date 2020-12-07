# coding=utf-8
"""Tests for Pulp`s download policies."""
from random import choice
import unittest

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.constants import ON_DEMAND_DOWNLOAD_POLICIES
from pulp_smash.pulp3.utils import (
    delete_orphans,
    gen_repo,
    get_added_content_summary,
    get_content_summary,
)

from pulp_file.tests.functional.constants import (
    FILE_FIXTURE_COUNT,
    FILE_FIXTURE_SUMMARY,
)
from pulp_file.tests.functional.utils import (
    core_client,
    gen_file_client,
    gen_file_remote,
    skip_if,
)
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401

from pulpcore.client.pulpcore import ArtifactsApi
from pulpcore.client.pulp_file import (
    ContentFilesApi,
    FileFilePublication,
    PublicationsFileApi,
    RepositoriesFileApi,
    RepositorySyncURL,
    RemotesFileApi,
)


class SyncPublishDownloadPolicyTestCase(unittest.TestCase):
    """Sync/Publish a repository with different download policies.

    This test targets the following issues:

    `Pulp #4126 <https://pulp.plan.io/issues/4126>`_
    `Pulp #4418 <https://pulp.plan.io/issues/4418>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.client = gen_file_client()
        cls.DP_ON_DEMAND = "on_demand" in ON_DEMAND_DOWNLOAD_POLICIES
        cls.DP_STREAMED = "streamed" in ON_DEMAND_DOWNLOAD_POLICIES

    @skip_if(bool, "DP_ON_DEMAND", False)
    def test_on_demand(self):
        """Sync with ``on_demand`` download policy. See :meth:`do_sync`."""
        self.do_sync("on_demand")
        self.do_publish("on_demand")

    @skip_if(bool, "DP_STREAMED", False)
    def test_streamed(self):
        """Sync with ``streamend`` download policy.  See :meth:`do_sync`."""
        self.do_sync("streamed")
        self.do_publish("streamed")

    def do_sync(self, download_policy):
        """Sync repositories with the different ``download_policy``.

        Do the following:

        1. Create a repository, and a remote.
        2. Assert that repository version is None.
        3. Sync the remote.
        4. Assert that repository version is not None.
        5. Assert that the correct number of possible units to be downloaded
           were shown.
        6. Sync the remote one more time in order to create another repository
           version.
        7. Assert that repository version is the same as the previous one.
        8. Assert that the same number of units are shown, and after the
           second sync no extra units should be shown, since the same remote
           was synced again.
        """
        # delete orphans to assure that no content units are present on the
        # file system
        delete_orphans()
        repo_api = RepositoriesFileApi(self.client)
        remote_api = RemotesFileApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        body = gen_file_remote(**{"policy": download_policy})
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
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = repo_api.read(repo.pulp_href)

        self.assertEqual(latest_version_href, repo.latest_version_href)
        self.assertDictEqual(get_content_summary(repo.to_dict()), FILE_FIXTURE_SUMMARY)

    def do_publish(self, download_policy):
        """Publish repository synced with lazy download policy."""
        repo_api = RepositoriesFileApi(self.client)
        remote_api = RemotesFileApi(self.client)
        publications = PublicationsFileApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        body = gen_file_remote(policy=download_policy)
        remote = remote_api.create(body)
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
        publication = publications.read(publication_href)
        self.assertIsNotNone(publication.repository_version, publication)


class LazySyncedContentAccessTestCase(unittest.TestCase):
    """Verify that lazy synced content can be acessed using content endpoint.

    Assert that one acessing lazy synced content using the content endpoint,
    e.g. ``http://localhost/pulp/api/v3/content/file/files`` will not raise an
    HTTP exception.

    This test targets the following issue:

    `Pulp #4463 <https://pulp.plan.io/issues/4463>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.client = gen_file_client()

    def test_on_demand(self):
        """Test ``on_demand``. See :meth:`do_test`."""
        self.do_test("on_demand")

    def test_streamed(self):
        """Test ``streamed``. See :meth:`do_test`."""
        self.do_test("streamed")

    def do_test(self, policy):
        """Access lazy synced content on using content endpoint."""
        # delete orphans to assure that no content units are present on the
        # file system
        delete_orphans()
        content_api = ContentFilesApi(self.client)
        repo_api = RepositoriesFileApi(self.client)
        remote_api = RemotesFileApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        body = gen_file_remote(**{"policy": policy})
        remote = remote_api.create(body)
        self.addCleanup(remote_api.delete, remote.pulp_href)

        # Sync the repository.
        self.assertEqual(repo.latest_version_href, f"{repo.pulp_href}versions/0/")
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        repo = repo_api.read(repo.pulp_href)

        # Assert that no HTTP error was raised.
        # Assert that the number of units present is according to the synced
        # feed.
        content = content_api.list().to_dict()["results"]
        self.assertEqual(len(content), FILE_FIXTURE_COUNT, content)


class SwitchDownloadPolicyTestCase(unittest.TestCase):
    """Perform a lazy sync, and change to immediate to force download.

    Perform an immediate sync to download artifacts for content units that
    are already created.

    This test case targets the following issue:

    * `Pulp #4467 <https://pulp.plan.io/issues/4467>`_
    """

    def test_all(self):
        """Perform a lazy sync and change to immeditae to force download."""
        # delete orphans to assure that no content units are present on the
        # file system
        delete_orphans()
        client = gen_file_client()
        artifacts_api = ArtifactsApi(core_client)
        repo_api = RepositoriesFileApi(client)
        remote_api = RemotesFileApi(client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        body = gen_file_remote(policy=choice(ON_DEMAND_DOWNLOAD_POLICIES))
        remote = remote_api.create(body)
        self.addCleanup(remote_api.delete, remote.pulp_href)

        # Sync the repository using a lazy download policy
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        artifacts = artifacts_api.list().to_dict()["results"]
        self.assertEqual(len(artifacts), 0, artifacts)

        # Update the policy to immediate
        response = remote_api.partial_update(remote.pulp_href, {"policy": "immediate"})
        monitor_task(response.task)
        remote = remote_api.read(remote.pulp_href)
        self.assertEqual(remote.policy, "immediate")

        # Sync using immediate download policy
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)

        # Assert that missing artifacts are downloaded
        artifacts = artifacts_api.list().to_dict()["results"]
        self.assertEqual(len(artifacts), FILE_FIXTURE_COUNT, artifacts)
