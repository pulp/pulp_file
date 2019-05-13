# coding=utf-8
"""Tests that verify download of content served by Pulp."""
import hashlib
import unittest
from random import choice
from urllib.parse import urljoin

from pulp_smash import api, config, utils
from pulp_smash.pulp3.constants import (
    LAZY_DOWNLOAD_POLICIES,
    REPO_PATH,
)
from pulp_smash.pulp3.utils import (
    download_content_unit,
    gen_distribution,
    gen_repo,
    sync,
)

from pulp_file.tests.functional.constants import (
    FILE_DISTRIBUTION_PATH,
    FILE_FIXTURE_URL,
    FILE_REMOTE_PATH,
)
from pulp_file.tests.functional.utils import (
    create_file_publication,
    gen_file_remote,
    get_file_content_paths,
)
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class DownloadContentTestCase(unittest.TestCase):
    """Verify whether content served by pulp can be downloaded."""

    def test_immediate(self):
        """Download content from Pulp. Content is synced with immediate.

        See :meth:`do_test`.
        """
        self.do_test('immediate')

    def test_lazy_download_policies(self):
        """Download content from Pulp. Content is synced with lazy policy.

        See :meth:`do_test`.

        This test targets the following issue:

        `Pulp #4496 <https://pulp.plan.io/issues/4496>`_
        """
        for policy in LAZY_DOWNLOAD_POLICIES:
            with self.subTest(policy):
                self.do_test(policy)

    def do_test(self, policy):
        """Verify whether content served by pulp can be downloaded.

        The process of publishing content is more involved in Pulp 3 than it
        was under Pulp 2. Given a repository, the process is as follows:

        1. Create a publication from the repository. (The latest repository
           version is selected if no version is specified.) A publication is a
           repository version plus metadata.
        2. Create a distribution from the publication. The distribution defines
           at which URLs a publication is available, e.g.
           ``http://example.com/content/foo/`` and
           ``http://example.com/content/bar/``.

        Do the following:

        1. Create, populate, publish, and distribute a repository.
        2. Select a random content unit in the distribution. Download that
           content unit from Pulp, and verify that the content unit has the
           same checksum when fetched directly from Pulp-Fixtures.

        This test targets the following issues:

        * `Pulp #2895 <https://pulp.plan.io/issues/2895>`_
        * `Pulp Smash #872 <https://github.com/PulpQE/pulp-smash/issues/872>`_
        """
        cfg = config.get_config()
        client = api.Client(cfg, api.json_handler)

        repo = client.post(REPO_PATH, gen_repo())
        self.addCleanup(client.delete, repo['_href'])

        body = gen_file_remote(policy=policy)
        remote = client.post(FILE_REMOTE_PATH, body)
        self.addCleanup(client.delete, remote['_href'])

        sync(cfg, remote, repo)
        repo = client.get(repo['_href'])

        # Create a publication.
        publication = create_file_publication(cfg, repo)
        self.addCleanup(client.delete, publication['_href'])

        # Create a distribution.
        body = gen_distribution()
        body['publication'] = publication['_href']
        distribution = client.using_handler(api.task_handler).post(
            FILE_DISTRIBUTION_PATH,
            body
        )
        self.addCleanup(client.delete, distribution['_href'])

        # Pick a file, and download it from both Pulp Fixtures…
        unit_path = choice(get_file_content_paths(repo))
        fixtures_hash = hashlib.sha256(
            utils.http_get(urljoin(FILE_FIXTURE_URL, unit_path))
        ).hexdigest()

        # …and Pulp.
        content = download_content_unit(cfg, distribution, unit_path)
        pulp_hash = hashlib.sha256(content).hexdigest()

        self.assertEqual(fixtures_hash, pulp_hash)
