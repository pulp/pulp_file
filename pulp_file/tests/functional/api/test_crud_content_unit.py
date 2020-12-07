# coding=utf-8
"""Tests that perform actions over content unit."""
import unittest

from pulp_smash import utils
from pulp_smash.pulp3.bindings import monitor_task, PulpTaskError
from pulp_smash.pulp3.utils import gen_repo, delete_orphans

from pulp_file.tests.functional.utils import (
    gen_artifact,
    gen_file_client,
    gen_file_content_attrs,
    gen_file_content_upload_attrs,
    tasks,
    skip_if,
)
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401

from pulpcore.client.pulp_file import (
    ContentFilesApi,
    RepositoriesFileApi,
    RepositoriesFileVersionsApi,
)


class ContentUnitTestCase(unittest.TestCase):
    """CRUD content unit.

    This test targets the following issues:

    * `Pulp #2872 <https://pulp.plan.io/issues/2872>`_
    * `Pulp #3445 <https://pulp.plan.io/issues/3445>`_
    * `Pulp Smash #870 <https://github.com/pulp/pulp-smash/issues/870>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variable."""
        delete_orphans()
        cls.content_unit = {}
        cls.file_content_api = ContentFilesApi(gen_file_client())
        cls.artifact = gen_artifact()

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        delete_orphans()

    def test_01_create_content_unit(self):
        """Create content unit."""
        attrs = gen_file_content_attrs(self.artifact)
        response = self.file_content_api.create(**attrs)
        created_resources = monitor_task(response.task).created_resources
        content_unit = self.file_content_api.read(created_resources[0])
        self.content_unit.update(content_unit.to_dict())
        for key, val in attrs.items():
            with self.subTest(key=key):
                self.assertEqual(self.content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_unit(self):
        """Read a content unit by its href."""
        content_unit = self.file_content_api.read(self.content_unit["pulp_href"]).to_dict()
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_units(self):
        """Read a content unit by its relative_path."""
        page = self.file_content_api.list(relative_path=self.content_unit["relative_path"])
        self.assertEqual(len(page.results), 1)
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(page.results[0].to_dict()[key], val)

    @skip_if(bool, "content_unit", False)
    def test_03_partially_update(self):
        """Attempt to update a content unit using HTTP PATCH.

        This HTTP method is not supported and a HTTP exception is expected.
        """
        attrs = gen_file_content_attrs(self.artifact)
        with self.assertRaises(AttributeError) as exc:
            self.file_content_api.partial_update(self.content_unit["pulp_href"], attrs)
        error_message = "'ContentFilesApi' object has no attribute 'partial_update'"
        self.assertEqual(exc.exception.args[0], error_message)

    @skip_if(bool, "content_unit", False)
    def test_03_fully_update(self):
        """Attempt to update a content unit using HTTP PUT.

        This HTTP method is not supported and a HTTP exception is expected.
        """
        attrs = gen_file_content_attrs(self.artifact)
        with self.assertRaises(AttributeError) as exc:
            self.file_content_api.update(self.content_unit["pulp_href"], attrs)
        error_message = "'ContentFilesApi' object has no attribute 'update'"
        self.assertEqual(exc.exception.args[0], error_message)

    @skip_if(bool, "content_unit", False)
    def test_04_delete(self):
        """Attempt to delete a content unit using HTTP DELETE.

        This HTTP method is not supported and a HTTP exception is expected.
        """
        with self.assertRaises(AttributeError) as exc:
            self.file_content_api.delete(self.content_unit["pulp_href"])
        error_message = "'ContentFilesApi' object has no attribute 'delete'"
        self.assertEqual(exc.exception.args[0], error_message)


class ContentUnitUploadTestCase(unittest.TestCase):
    """CRUD content unit with upload feature.

    This test targets the following issue:

    `Pulp #5403 <https://pulp.plan.io/issues/5403>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variable."""
        delete_orphans()
        cls.content_unit = {}
        cls.file_content_api = ContentFilesApi(gen_file_client())
        cls.attrs = gen_file_content_upload_attrs()

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        delete_orphans()

    def test_01_create_content_unit(self):
        """Create content unit."""
        response = self.file_content_api.create(**self.attrs, file=__file__)
        created_resources = monitor_task(response.task).created_resources
        content_unit = self.file_content_api.read(created_resources[0])
        self.content_unit.update(content_unit.to_dict())
        for key, val in self.attrs.items():
            with self.subTest(key=key):
                self.assertEqual(self.content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_unit(self):
        """Read a content unit by its href."""
        content_unit = self.file_content_api.read(self.content_unit["pulp_href"]).to_dict()
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(content_unit[key], val)

    @skip_if(bool, "content_unit", False)
    def test_02_read_content_units(self):
        """Read a content unit by its relative_path."""
        page = self.file_content_api.list(relative_path=self.content_unit["relative_path"])
        self.assertEqual(len(page.results), 1)
        for key, val in self.content_unit.items():
            with self.subTest(key=key):
                self.assertEqual(page.results[0].to_dict()[key], val)

    @skip_if(bool, "content_unit", False)
    def test_03_fail_duplicate_content_unit(self):
        """Create content unit."""
        response = self.file_content_api.create(**self.attrs, file=__file__)
        with self.assertRaises(PulpTaskError) as cm:
            monitor_task(response.task)
        task = cm.exception.task.to_dict()
        self.assertEqual(task["state"], "failed")
        error_description = task["error"]["description"]
        for key in ("already", "relative", "path", "digest"):
            self.assertIn(key, error_description.lower(), task["error"])

    @skip_if(bool, "content_unit", False)
    def test_03_duplicate_content_unit(self):
        """Create content unit."""
        attrs = self.attrs.copy()
        attrs["relative_path"] = utils.uuid4()
        response = self.file_content_api.create(**attrs, file=__file__)
        monitor_task(response.task)


class DuplicateContentUnit(unittest.TestCase):
    """Attempt to create a duplicate content unit.

    This test targets the following issues:

    *  `Pulp #4125 <https://pulp.plan.io/issue/4125>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.file_content_api = ContentFilesApi(gen_file_client())

    @classmethod
    def tearDownClass(cls):
        """Clean created resources."""
        delete_orphans()

    def test_raise_error(self):
        """Create a duplicate content unit using same relative_path.

        Artifacts are unique by ``relative_path`` and ``file``.

        In order to raise an HTTP error, the same ``artifact`` and the same
        ``relative_path`` should be used.
        """
        delete_orphans()
        artifact = gen_artifact()
        attrs = gen_file_content_attrs(artifact)

        # create first content unit.
        response = self.file_content_api.create(**attrs)
        monitor_task(response.task)

        # using the same attrs used to create the first content unit.
        response = self.file_content_api.create(**attrs)
        with self.assertRaises(PulpTaskError) as cm:
            monitor_task(response.task)
        error = cm.exception.task.to_dict()["error"]
        for key in ("already", "relative", "path", "digest"):
            self.assertIn(key, error["description"].lower(), error)

    def test_non_error(self):
        """Create a duplicate content unit with different relative_path.

        Artifacts are unique by ``relative_path`` and ``file``.

        In order to avoid an HTTP error, use the same ``artifact`` and
        different ``relative_path``.
        """
        delete_orphans()
        artifact = gen_artifact()

        # create first content unit.
        response = self.file_content_api.create(**gen_file_content_attrs(artifact))
        monitor_task(response.task)

        # create second content unit.
        response = self.file_content_api.create(**gen_file_content_attrs(artifact))
        monitor_task(response.task)
        task = tasks.read(response.task)
        self.assertEqual(task.state, "completed")


class DuplicateRelativePathsInRepo(unittest.TestCase):
    """Associate different Content units with the same ``relative_path`` in one RepositoryVersion.

    This test targets the following issues:

    *  `Pulp #4028 <https://pulp.plan.io/issue/4028>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.client = gen_file_client()

    @classmethod
    def tearDownClass(cls):
        """Clean created resources."""
        delete_orphans()

    def test_second_unit_replaces_the_first(self):
        """Create a duplicate content unit with different ``artifacts`` and same ``relative_path``.

        Artifacts are unique by ``relative_path`` and ``file``.
        """
        delete_orphans()
        content_api = ContentFilesApi(self.client)
        repo_api = RepositoriesFileApi(self.client)
        versions_api = RepositoriesFileVersionsApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        artifact = gen_artifact()

        # create first content unit.
        content_attrs = gen_file_content_attrs(artifact)
        content_attrs["repository"] = repo.pulp_href
        response = content_api.create(**content_attrs)
        monitor_task(response.task)

        artifact = gen_artifact(file=__file__)

        # create second content unit.
        second_content_attrs = gen_file_content_attrs(artifact)
        second_content_attrs["repository"] = repo.pulp_href
        second_content_attrs["relative_path"] = content_attrs["relative_path"]

        response = content_api.create(**second_content_attrs)
        monitor_task(response.task)

        repo_latest_version = versions_api.read(repo_api.read(repo.pulp_href).latest_version_href)

        self.assertEqual(repo_latest_version.content_summary.present["file.file"]["count"], 1)

    def test_second_unit_raises_error(self):
        """Create a duplicate content unit with different ``artifacts`` and same ``relative_path``.

        Artifacts are unique by ``relative_path`` and ``file``.
        """
        delete_orphans()
        content_api = ContentFilesApi(self.client)
        repo_api = RepositoriesFileApi(self.client)

        repo = repo_api.create(gen_repo())
        self.addCleanup(repo_api.delete, repo.pulp_href)

        artifact = gen_artifact()

        # create first content unit.
        content_attrs = gen_file_content_attrs(artifact)
        response = content_api.create(**content_attrs)
        monitor_task(response.task)

        artifact = gen_artifact(file=__file__)

        # create second content unit.
        second_content_attrs = gen_file_content_attrs(artifact)
        second_content_attrs["relative_path"] = content_attrs["relative_path"]
        response = content_api.create(**second_content_attrs)
        monitor_task(response.task)

        data = {"add_content_units": [c.pulp_href for c in content_api.list().results]}
        response = repo_api.modify(repo.pulp_href, data)
        with self.assertRaises(PulpTaskError) as cm:
            monitor_task(response.task)
        task = cm.exception.task.to_dict()

        error_message = (
            "Cannot create repository version. "
            "More than one file.file content with "
            "the duplicate values for relative_path."
        )
        self.assertEqual(task["error"]["description"], error_message)
