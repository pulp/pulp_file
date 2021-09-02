import unittest

from pulp_smash import config
from pulp_smash.pulp3.bindings import delete_orphans

from pulpcore.client.pulp_file import AcsFileApi, RemotesFileApi
from pulpcore.client.pulp_file.exceptions import ApiException

from pulpcore.tests.functional.api.using_plugin.utils import (
    gen_file_client,
    gen_file_remote,
)


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
        cls.file_remote_api = RemotesFileApi(cls.file_client)
        cls.file_acs_api = AcsFileApi(cls.file_client)
        cls.paths = ["goodpath/PULP_MANIFEST", "test", "whatever/test"]

    @classmethod
    def tearDownClass(cls):
        """Run orphan cleanup."""
        delete_orphans()

    def test_path_validation(self):
        """Test the validation of paths."""
        remote = self.file_remote_api.create(gen_file_remote(policy="on_demand"))
        self.addCleanup(self.file_remote_api.delete, remote.pulp_href)

        # one path is wrong, begins with /
        acs_data = {
            "name": "alternatecontentsource",
            "remote": remote.pulp_href,
            "paths": self.paths + ["/bad_path"],
        }

        with self.assertRaises(ApiException) as ctx:
            acs = self.file_acs_api.create(acs_data)
        self.assertEqual(ctx.exception.status, 400)

        # use valid paths
        acs_data["paths"] = self.paths
        acs = self.file_acs_api.create(acs_data)
        self.addCleanup(self.file_acs_api.delete, acs.pulp_href)
        self.assertEqual(sorted(acs.paths), sorted(self.paths))
