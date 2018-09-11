# coding=utf-8
"""Tests that CRUD remotes."""
from random import choice
import unittest

from requests.exceptions import HTTPError

from pulp_smash import api, config, utils
from pulp_smash.pulp3.constants import REPO_PATH
from pulp_smash.pulp3.utils import gen_repo

from pulp_file.tests.functional.constants import (
    FILE_FIXTURE_URL,
    FILE2_FIXTURE_URL,
    FILE_REMOTE_PATH
)
from pulp_file.tests.functional.utils import gen_file_remote, skip_if
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class CRUDRemotesTestCase(unittest.TestCase):
    """CRUD remotes."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables.

        In order to create a remote a repository has to be created first.
        """
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)
        cls.remote = {}
        cls.repo = cls.client.post(REPO_PATH, gen_repo())

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        cls.client.delete(cls.repo['_href'])

    def test_01_create_remote(self):
        """Create a remote."""
        body = _gen_verbose_remote()
        type(self).remote = self.client.post(FILE_REMOTE_PATH, body)
        for key in ('username', 'password'):
            del body[key]
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote[key], val)

    @skip_if(bool, 'remote', False)
    def test_02_create_same_name(self):
        """Try to create a second remote with an identical name.

        See: `Pulp Smash #1055
        <https://github.com/PulpQE/pulp-smash/issues/1055>`_.
        """
        body = gen_file_remote()
        body['name'] = self.remote['name']
        with self.assertRaises(HTTPError):
            self.client.post(FILE_REMOTE_PATH, body)

    @skip_if(bool, 'remote', False)
    def test_02_read_remote(self):
        """Read a remote by its href."""
        remote = self.client.get(self.remote['_href'])
        for key, val in self.remote.items():
            with self.subTest(key=key):
                self.assertEqual(remote[key], val)

    @skip_if(bool, 'remote', False)
    def test_02_read_remotes(self):
        """Read a remote by its name."""
        page = self.client.get(FILE_REMOTE_PATH, params={
            'name': self.remote['name']
        })
        self.assertEqual(len(page['results']), 1)
        for key, val in self.remote.items():
            with self.subTest(key=key):
                self.assertEqual(page['results'][0][key], val)

    @skip_if(bool, 'remote', False)
    def test_03_partially_update(self):
        """Update a remote using HTTP PATCH."""
        body = _gen_verbose_remote()
        self.client.patch(self.remote['_href'], body)
        for key in ('username', 'password'):
            del body[key]
        type(self).remote = self.client.get(self.remote['_href'])
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote[key], val)

    @skip_if(bool, 'remote', False)
    def test_04_fully_update(self):
        """Update a remote using HTTP PUT."""
        body = _gen_verbose_remote()
        self.client.put(self.remote['_href'], body)
        for key in ('username', 'password'):
            del body[key]
        type(self).remote = self.client.get(self.remote['_href'])
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote[key], val)

    @skip_if(bool, 'remote', False)
    def test_05_delete(self):
        """Delete a remote."""
        self.client.delete(self.remote['_href'])
        with self.assertRaises(HTTPError):
            self.client.get(self.remote['_href'])


class CreateRemoteNoURLTestCase(unittest.TestCase):
    """Verify whether is possible to create a remote without a URL."""

    def test_all(self):
        """Verify whether is possible to create a remote without a URL.

        This test targets the following issues:

        * `Pulp #3395 <https://pulp.plan.io/issues/3395>`_
        * `Pulp Smash #984 <https://github.com/PulpQE/pulp-smash/issues/984>`_
        """
        body = gen_file_remote(url=utils.uuid4())
        del body['url']
        with self.assertRaises(HTTPError):
            api.Client(config.get_config()).post(FILE_REMOTE_PATH, body)


def _gen_verbose_remote():
    """Return a semi-random dict for use in defining a remote.

    For most tests, it's desirable to create remotes with as few attributes
    as possible, so that the tests can specifically target and attempt to break
    specific features. This module specifically targets remotes, so it makes
    sense to provide as many attributes as possible.

    Note that 'username' and 'password' are write-only attributes.
    """
    attrs = gen_file_remote(url=choice((FILE_FIXTURE_URL, FILE2_FIXTURE_URL)))
    attrs.update({
        'password': utils.uuid4(),
        'username': utils.uuid4(),
        'validate': choice((False, True)),
    })
    return attrs
