# coding=utf-8
"""Tests that perform actions over content unit."""
import unittest

from requests.exceptions import HTTPError

from pulp_smash import api, config, utils
from pulp_smash.exceptions import TaskReportError
from pulp_smash.pulp3.constants import ARTIFACTS_PATH
from pulp_smash.pulp3.utils import delete_orphans, gen_repo

from pulp_file.tests.functional.constants import (
    FILE_REPO_PATH,
    FILE_CONTENT_PATH,
    FILE_URL,
    FILE_URL2,
)

from pulp_file.tests.functional.utils import (
    gen_file_content_attrs,
    gen_file_content_upload_attrs,
    skip_if,
)
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class ContentUnitTestCase(unittest.TestCase):
    """CRUD content unit.

    This test targets the following issues:

    * `Pulp #2872 <https://pulp.plan.io/issues/2872>`_
    * `Pulp #3445 <https://pulp.plan.io/issues/3445>`_
    * `Pulp Smash #870 <https://github.com/PulpQE/pulp-smash/issues/870>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variable."""
        cls.cfg = config.get_config()
        delete_orphans(cls.cfg)
        cls.content_unit = {}
        cls.client = api.Client(cls.cfg, api.json_handler)
        files = {"file": utils.http_get(FILE_URL)}
        cls.artifact = cls.client.post(ARTIFACTS_PATH, files=files)

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        delete_orphans(cls.cfg)

    def test_01_create_content_unit(self):
        """Create content unit."""
        attrs = gen_file_content_attrs(self.artifact)
        call_report = self.client.post(FILE_CONTENT_PATH, data=attrs)
        created_resources = next(api.poll_spawned_tasks(self.cfg, call_report))["created_resources"]
        self.content_unit.update(self.client.get(created_resources[0]))
        for key, val in attrs.items():
            with self.subTest(key=key):
                self.assertEqual(self.content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_unit(self):
        """Read a content unit by its href."""
        content_unit = self.client.get(self.content_unit["pulp_href"])
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_units(self):
        """Read a content unit by its relative_path."""
        page = self.client.get(
            FILE_CONTENT_PATH, params={"relative_path": self.content_unit["relative_path"]}
        )
        self.assertEqual(len(page["results"]), 1)
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(page["results"][0][key], val)

    @skip_if(bool, "content_unit", False)
    def test_03_partially_update(self):
        """Attempt to update a content unit using HTTP PATCH.

        This HTTP method is not supported and a HTTP exception is expected.
        """
        attrs = gen_file_content_attrs(self.artifact)
        with self.assertRaises(HTTPError) as exc:
            self.client.patch(self.content_unit["pulp_href"], attrs)
        self.assertEqual(exc.exception.response.status_code, 405)

    @skip_if(bool, "content_unit", False)
    def test_03_fully_update(self):
        """Attempt to update a content unit using HTTP PUT.

        This HTTP method is not supported and a HTTP exception is expected.
        """
        attrs = gen_file_content_attrs(self.artifact)
        with self.assertRaises(HTTPError) as exc:
            self.client.put(self.content_unit["pulp_href"], attrs)
        self.assertEqual(exc.exception.response.status_code, 405)

    @skip_if(bool, "content_unit", False)
    def test_04_delete(self):
        """Attempt to delete a content unit using HTTP DELETE.

        This HTTP method is not supported and a HTTP exception is expected.
        """
        with self.assertRaises(HTTPError) as exc:
            self.client.delete(self.content_unit["pulp_href"])
        self.assertEqual(exc.exception.response.status_code, 405)


class ContentUnitUploadTestCase(unittest.TestCase):
    """CRUD content unit with upload feature.

    This test targets the following issue:

    `Pulp #5403 <https://pulp.plan.io/issues/5403>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variable."""
        cls.cfg = config.get_config()
        delete_orphans(cls.cfg)
        cls.content_unit = {}
        cls.client = api.Client(cls.cfg, api.smart_handler)
        cls.files = {"file": utils.http_get(FILE_URL)}
        cls.attrs = gen_file_content_upload_attrs()

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        delete_orphans(cls.cfg)

    def test_01_create_content_unit(self):
        """Create content unit."""
        content_unit = self.client.post(FILE_CONTENT_PATH, data=self.attrs, files=self.files)
        self.content_unit.update(content_unit)
        for key, val in self.attrs.items():
            with self.subTest(key=key):
                self.assertEqual(self.content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_unit(self):
        """Read a content unit by its href."""
        content_unit = self.client.get(self.content_unit["pulp_href"])
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_units(self):
        """Read a content unit by its relative_path."""
        page = self.client.using_handler(api.json_handler).get(
            FILE_CONTENT_PATH, params={"relative_path": self.content_unit["relative_path"]}
        )
        self.assertEqual(len(page["results"]), 1)
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(page["results"][0][key], val)

    @skip_if(bool, "content_unit", False)
    def test_03_fail_duplicate_content_unit(self):
        """Create content unit."""
        with self.assertRaises(TaskReportError) as exc:
            self.client.post(FILE_CONTENT_PATH, data=self.attrs, files=self.files)
        self.assertEqual(exc.exception.task["state"], "failed")
        error = exc.exception.task["error"]
        for key in ("already", "relative", "path", "digest"):
            self.assertIn(key, error["description"].lower(), error)

    @skip_if(bool, "content_unit", False)
    def test_03_duplicate_content_unit(self):
        """Create content unit."""
        attrs = self.attrs.copy()
        attrs["relative_path"] = utils.uuid4()
        self.client.post(FILE_CONTENT_PATH, data=attrs, files=self.files)


class DuplicateContentUnit(unittest.TestCase):
    """Attempt to create a duplicate content unit.

    This test targets the following issues:

    *  `Pulp #4125 <https://pulp.plan.io/issue/4125>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)

    @classmethod
    def tearDownClass(cls):
        """Clean created resources."""
        delete_orphans(cls.cfg)

    def test_raise_error(self):
        """Create a duplicate content unit using same relative_path.

        Artifacts are unique by ``relative_path`` and ``file``.

        In order to raise an HTTP error, the same ``artifact`` and the same
        ``relative_path`` should be used.
        """
        delete_orphans(self.cfg)
        files = {"file": utils.http_get(FILE_URL)}
        artifact = self.client.post(ARTIFACTS_PATH, files=files)
        attrs = gen_file_content_attrs(artifact)

        # create first content unit.
        self.client.post(FILE_CONTENT_PATH, attrs)

        # using the same attrs used to create the first content unit.
        with self.assertRaises(TaskReportError) as exc:
            self.client.post(FILE_CONTENT_PATH, attrs)
        self.assertEqual(exc.exception.task["state"], "failed")
        error = exc.exception.task["error"]
        for key in ("already", "relative", "path", "digest"):
            self.assertIn(key, error["description"].lower(), error)

    def test_non_error(self):
        """Create a duplicate content unit with different relative_path.

        Artifacts are unique by ``relative_path`` and ``file``.

        In order to avoid an HTTP error, use the same ``artifact`` and
        different ``relative_path``.
        """
        delete_orphans(self.cfg)
        files = {"file": utils.http_get(FILE_URL)}
        artifact = self.client.post(ARTIFACTS_PATH, files=files)

        # create first content unit.
        self.client.post(FILE_CONTENT_PATH, gen_file_content_attrs(artifact))

        # create second content unit.
        self.client.post(FILE_CONTENT_PATH, gen_file_content_attrs(artifact))


class DuplicateRelativePathsInRepo(unittest.TestCase):
    """Associate different Content units with the same ``relative_path`` in one RepositoryVersion.

    This test targets the following issues:

    *  `Pulp #4028 <https://pulp.plan.io/issue/4028>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)

    @classmethod
    def tearDownClass(cls):
        """Clean created resources."""
        delete_orphans(cls.cfg)

    def test_second_unit_replaces_the_first(self):
        """Create a duplicate content unit with different ``artifacts`` and same ``relative_path``.

        Artifacts are unique by ``relative_path`` and ``file``.
        """
        delete_orphans(self.cfg)

        repo = self.client.post(FILE_REPO_PATH, gen_repo())
        self.addCleanup(self.client.delete, repo["pulp_href"])

        files = {"file": utils.http_get(FILE_URL)}
        artifact = self.client.post(ARTIFACTS_PATH, files=files)

        # create first content unit.
        content_attrs = gen_file_content_attrs(artifact)
        content_attrs["repository"] = repo["pulp_href"]
        self.client.post(FILE_CONTENT_PATH, content_attrs)

        files = {"file": utils.http_get(FILE_URL2)}
        artifact = self.client.post(ARTIFACTS_PATH, files=files)

        # create second content unit.
        second_content_attrs = gen_file_content_attrs(artifact)
        second_content_attrs["repository"] = repo["pulp_href"]
        second_content_attrs["relative_path"] = content_attrs["relative_path"]

        self.client.post(FILE_CONTENT_PATH, second_content_attrs)

        repo_latest_version = self.client.get(
            self.client.get(repo["pulp_href"])["latest_version_href"]
        )

        self.assertEqual(repo_latest_version["content_summary"]["present"]["file.file"]["count"], 1)
