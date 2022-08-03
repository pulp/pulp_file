"""Tests that perform actions over distributions."""
import unittest

from pulp_smash import api, config, utils
from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.utils import (
    gen_distribution,
    gen_repo,
    get_content,
    get_versions,
    modify_repo,
    sync,
)
from requests.exceptions import HTTPError

from pulp_file.tests.functional.utils import (
    create_file_publication,
    gen_file_remote,
)
from .constants import (
    BASE_DISTRIBUTION_PATH,
    FILE_CONTENT_NAME,
    FILE_DISTRIBUTION_PATH,
    FILE_REMOTE_PATH,
    FILE_REPO_PATH,
)


class CRUDPublicationDistributionTestCase(unittest.TestCase):
    """CRUD Publication Distribution."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg)

    def setUp(self):
        """Arrange the test."""
        self.attr = (
            "name",
            "base_path",
        )
        self.distribution = {}
        self.publication = {}
        self.remote = {}
        self.repo = {}

    def tearDown(self):
        """Clean variables."""
        for resource in (self.publication, self.remote, self.repo):
            if resource:
                self.client.delete(resource["pulp_href"])

    def test_crud_workflow(self):
        self._create()
        self._read()
        self._partially_update()
        self._fully_update()
        self._list()
        self._delete_distribution()

    def _create(self):
        """Create a publication distribution.

        Do the following:

        1. Create a repository and 3 repository versions with at least 1 file
           content in it. Create a publication using the second repository
           version.
        2. Create a distribution with 'publication' field set to
           the publication from step (1).
        3. Assert the distribution got created correctly with the correct
           base_path, name, and publication. Assert that content guard is
           unset.
        4. Assert that publication has a 'distributions' reference to the
           distribution (it's backref).

        """
        self.repo.update(self.client.post(FILE_REPO_PATH, gen_repo()))
        self.remote.update(self.client.post(FILE_REMOTE_PATH, gen_file_remote()))
        # create 3 repository versions
        sync(self.cfg, self.remote, self.repo)
        self.repo = self.client.get(self.repo["pulp_href"])
        for file_content in get_content(self.repo)[FILE_CONTENT_NAME]:
            modify_repo(self.cfg, self.repo, remove_units=[file_content])

        self.repo = self.client.get(self.repo["pulp_href"])

        versions = get_versions(self.repo)

        self.publication.update(
            create_file_publication(self.cfg, self.repo, versions[1]["pulp_href"])
        )

        self.distribution.update(
            self.client.post(
                FILE_DISTRIBUTION_PATH, gen_distribution(publication=self.publication["pulp_href"])
            )
        )

        self.publication = self.client.get(self.publication["pulp_href"])

        # content_guard and repository parameters unset.
        for key, val in self.distribution.items():
            if key in ["content_guard", "repository"]:
                self.assertIsNone(val, self.distribution)
            else:
                self.assertIsNotNone(val, self.distribution)

        self.assertEqual(
            self.distribution["publication"], self.publication["pulp_href"], self.distribution
        )

        self.assertEqual(
            self.publication["distributions"][0], self.distribution["pulp_href"], self.publication
        )

    def _read(self):
        """Read distribution by its href."""
        distribution = self.client.get(self.distribution["pulp_href"])
        for key, val in self.distribution.items():
            with self.subTest(key=key):
                self.assertEqual(distribution[key], val)

    def _partially_update(self):
        """Update a distribution using PATCH."""
        for key in self.attr:
            with self.subTest(key=key):
                self._do_partially_update_attr(key)

    def _fully_update(self):
        """Update a distribution using PUT."""
        for key in self.attr:
            with self.subTest(key=key):
                self._do_fully_update_attr(key)

    def _list(self):
        """Test the generic distribution list endpoint."""
        distributions = self.client.get(BASE_DISTRIBUTION_PATH)
        assert self.distribution["pulp_href"] in [distro["pulp_href"] for distro in distributions]

    def _delete_distribution(self):
        """Delete a distribution."""
        self.client.delete(self.distribution["pulp_href"])
        with self.assertRaises(HTTPError):
            self.client.get(self.distribution["pulp_href"])

    def _do_fully_update_attr(self, attr):
        """Update a distribution attribute using HTTP PUT.

        :param attr: The name of the attribute to update.
        """
        distribution = self.client.get(self.distribution["pulp_href"])
        string = utils.uuid4()
        distribution[attr] = string
        self.client.put(distribution["pulp_href"], distribution)

        # verify the update
        distribution = self.client.get(distribution["pulp_href"])
        self.assertEqual(string, distribution[attr], distribution)

    def _do_partially_update_attr(self, attr):
        """Update a distribution using HTTP PATCH.

        :param attr: The name of the attribute to update.
        """
        string = utils.uuid4()
        self.client.patch(self.distribution["pulp_href"], {attr: string})

        # Verify the update
        distribution = self.client.get(self.distribution["pulp_href"])
        self.assertEqual(string, distribution[attr], self.distribution)


class DistributionBasePathTestCase(unittest.TestCase):
    """Test possible values for ``base_path`` on a distribution."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg)

    def setUp(self):
        """Set up resources."""
        body = gen_distribution()
        body["base_path"] = body["base_path"].replace("-", "/")
        self.distribution = self.client.post(FILE_DISTRIBUTION_PATH, body)

    def tearDown(self):
        """Clean up resources."""
        response = self.client.delete(self.distribution["pulp_href"])
        monitor_task(response["pulp_href"])

    def test_negative_create_using_spaces(self):
        """Test that spaces can not be part of ``base_path``."""
        self.try_create_distribution(base_path=utils.uuid4().replace("-", " "))
        self.try_update_distribution(base_path=utils.uuid4().replace("-", " "))

    def test_negative_create_using_begin_slash(self):
        """Test that slash cannot be in the begin of ``base_path``."""
        self.try_create_distribution(base_path="/" + utils.uuid4())
        self.try_update_distribution(base_path="/" + utils.uuid4())

    def test_negative_create_using_end_slash(self):
        """Test that slash cannot be in the end of ``base_path``."""
        self.try_create_distribution(base_path=utils.uuid4() + "/")
        self.try_update_distribution(base_path=utils.uuid4() + "/")

    def test_negative_create_using_non_unique_base_path(self):
        """Test that ``base_path`` can not be duplicated."""
        self.try_create_distribution(base_path=self.distribution["base_path"])

    def test_negative_create_using_overlapping_base_path(self):
        """Test that distributions can't have overlapping ``base_path``.

        See: `Pulp #2987`_.
        """
        base_path = self.distribution["base_path"].rsplit("/", 1)[0]
        self.try_create_distribution(base_path=base_path)

        base_path = "/".join((self.distribution["base_path"], utils.uuid4().replace("-", "/")))
        self.try_create_distribution(base_path=base_path)

    def try_create_distribution(self, **kwargs):
        """Unsuccessfully create a distribution.

        Merge the given kwargs into the body of the request.
        """
        body = gen_distribution()
        body.update(kwargs)
        with self.assertRaises(HTTPError) as ctx:
            self.client.post(FILE_DISTRIBUTION_PATH, body)

        self.assertIsNotNone(
            ctx.exception.response.json()["base_path"], ctx.exception.response.json()
        )

    def try_update_distribution(self, **kwargs):
        """Unsuccessfully update a distribution with HTTP PATCH.

        Use the given kwargs as the body of the request.
        """
        with self.assertRaises(HTTPError) as ctx:
            self.client.patch(self.distribution["pulp_href"], kwargs)

        self.assertIsNotNone(
            ctx.exception.response.json()["base_path"], ctx.exception.response.json()
        )
