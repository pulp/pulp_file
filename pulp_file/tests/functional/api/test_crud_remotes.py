"""Tests that CRUD file remotes."""
import json
from random import choice
import unittest

from pulp_smash import utils

from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.constants import ON_DEMAND_DOWNLOAD_POLICIES

from pulp_file.tests.functional.constants import (
    FILE_FIXTURE_MANIFEST_URL,
    FILE2_FIXTURE_MANIFEST_URL,
)
from pulp_file.tests.functional.utils import (
    gen_file_client,
    gen_file_remote,
)

from pulpcore.client.pulp_file import RemotesFileApi
from pulpcore.client.pulp_file.exceptions import ApiException


class CRUDRemotesTestCase(unittest.TestCase):
    """CRUD remotes."""

    @classmethod
    def setUpClass(cls):
        cls.remote_api = RemotesFileApi(gen_file_client())

    def test_workflow(self):
        self._create_remote()
        self._create_same_name()
        self._read_remote()
        self._read_remotes()
        self._partially_update()
        self._fully_update()
        self._delete()

    def _create_remote(self):
        """Create a remote."""
        body = _gen_verbose_remote()
        self.remote = self.remote_api.create(body)
        for key in ("username", "password"):
            del body[key]
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote.to_dict()[key], val, key)

    def _create_same_name(self):
        """Try to create a second remote with an identical name.

        See: `Pulp Smash #1055
        <https://github.com/pulp/pulp-smash/issues/1055>`_.
        """
        body = gen_file_remote()
        body["name"] = self.remote.name
        with self.assertRaises(ApiException):
            self.remote_api.create(body)

    def _read_remote(self):
        """Read a remote by its href."""
        remote = self.remote_api.read(self.remote.pulp_href)
        for key, val in self.remote.to_dict().items():
            with self.subTest(key=key):
                self.assertEqual(remote.to_dict()[key], val, key)

    def _read_remotes(self):
        """Read a remote by its name."""
        page = self.remote_api.list(name=self.remote.name)
        self.assertEqual(len(page.results), 1)
        for key, val in self.remote.to_dict().items():
            with self.subTest(key=key):
                self.assertEqual(page.results[0].to_dict()[key], val, key)

    def _partially_update(self):
        """Update a remote using HTTP PATCH."""
        body = _gen_verbose_remote()
        response = self.remote_api.partial_update(self.remote.pulp_href, body)
        monitor_task(response.task)
        for key in ("username", "password"):
            del body[key]
        self.remote = self.remote_api.read(self.remote.pulp_href)
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote.to_dict()[key], val, key)

    def _fully_update(self):
        """Update a remote using HTTP PUT."""
        body = _gen_verbose_remote()
        response = self.remote_api.update(self.remote.pulp_href, body)
        monitor_task(response.task)
        for key in ("username", "password"):
            del body[key]
        self.remote = self.remote_api.read(self.remote.pulp_href)
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote.to_dict()[key], val, key)

    def _delete(self):
        """Delete a remote."""
        response = self.remote_api.delete(self.remote.pulp_href)
        monitor_task(response.task)
        with self.assertRaises(ApiException):
            self.remote_api.read(self.remote.pulp_href)

    def test_negative_create_file_remote_with_invalid_parameter(self):
        """Attempt to create file remote passing invalid parameter."""
        with self.assertRaises(ApiException) as exc:
            RemotesFileApi(gen_file_client()).create(gen_file_remote(foo="bar"))

        assert exc.exception.status == 400
        assert json.loads(exc.exception.body)["foo"] == ["Unexpected field"]


class CreateRemoteNoURLTestCase(unittest.TestCase):
    """Verify whether is possible to create a remote without a URL."""

    def test_all(self):
        """Verify whether is possible to create a remote without a URL.

        This test targets the following issues:

        * `Pulp #3395 <https://pulp.plan.io/issues/3395>`_
        * `Pulp Smash #984 <https://github.com/pulp/pulp-smash/issues/984>`_
        """
        body = gen_file_remote()
        del body["url"]
        with self.assertRaises(ApiException):
            RemotesFileApi(gen_file_client()).create(body)


class RemoteDownloadPolicyTestCase(unittest.TestCase):
    """Verify download policy behavior for valid and invalid values."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.remote_api = RemotesFileApi(gen_file_client())
        cls.policies = ON_DEMAND_DOWNLOAD_POLICIES

    def setUp(self):
        self.remote = {}
        self.body = _gen_verbose_remote()

    def test_workflow(self):
        self._no_defined_policy()
        self._change_policy()
        self._invalid_policy()

    def _no_defined_policy(self):
        """Verify the default policy `immediate`."""
        del self.body["policy"]
        self.remote = self.remote_api.create(self.body).to_dict()
        self.addCleanup(self.remote_api.delete, self.remote["pulp_href"])
        assert self.remote["policy"] == "immediate"

    def _change_policy(self):
        """Verify ability to change policy to value other than the default.

        Update the remote policy to a valid value other than `immedaite`
        and verify the new set value.
        """
        changed_policy = choice([item for item in self.policies if item != "immediate"])
        response = self.remote_api.partial_update(
            self.remote["pulp_href"], {"policy": changed_policy}
        )
        monitor_task(response.task)
        self.remote.update(self.remote_api.read(self.remote["pulp_href"]).to_dict())
        self.assertEqual(self.remote["policy"], changed_policy, self.remote)

    def _invalid_policy(self):
        """Verify an invalid policy does not update the remote policy.

        Get the current remote policy.
        Attempt to update the remote policy to an invalid value.
        Verify the policy remains the same.
        """
        remote = self.remote_api.read(self.remote["pulp_href"]).to_dict()
        with self.assertRaises(ApiException):
            self.remote_api.partial_update(self.remote["pulp_href"], {"policy": utils.uuid4()})
        self.remote.update(self.remote_api.read(self.remote["pulp_href"]).to_dict())
        self.assertEqual(remote["policy"], self.remote["policy"], self.remote)


def _gen_verbose_remote():
    """Return a semi-random dict for use in defining a remote.

    For most tests, it"s desirable to create remotes with as few attributes
    as possible, so that the tests can specifically target and attempt to break
    specific features. This module specifically targets remotes, so it makes
    sense to provide as many attributes as possible.

    Note that 'username' and 'password' are write-only attributes.
    """
    attrs = gen_file_remote(url=choice((FILE_FIXTURE_MANIFEST_URL, FILE2_FIXTURE_MANIFEST_URL)))
    attrs.update(
        {
            "password": utils.uuid4(),
            "username": utils.uuid4(),
            "policy": choice(ON_DEMAND_DOWNLOAD_POLICIES),
        }
    )
    return attrs
