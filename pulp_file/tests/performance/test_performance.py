import os
import glob
import errno
import csv
import hashlib
import datetime
import multiprocessing

from collections import namedtuple
from django.test import TestCase

from .pulpperf import interact
from .pulpperf import utils
from .pulpperf import reporting

DIRECTORY = "/usr/local/lib/pulp/lib/python3.7/site-packages/rest_framework/static/fixtures/"
FILES_COUNT = 100000
FILE_PREFIX = "a"
FILE_SIZE = 50

Args = namedtuple("Arguments", "limit processes repositories")


class PerformanceTestCase(TestCase):
    """
    Test case for running performance tests.

    The tests are ported from https://github.com/redhat-performance/pulpperf.
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        super().setUpClass()
        manifests_dumper = ManifestsDumper(DIRECTORY, FILES_COUNT, FILE_PREFIX, FILE_SIZE)
        manifests_dumper.generate_manifests()

        cls.args = Args(
            limit=100, processes=1, repositories=["http://localhost:80/static/fixtures/"]
        )
        cls.data = []

    @classmethod
    def tearDownClass(cls):
        """Clean-up generated manifests."""
        super().tearDownClass()
        manifests_cleaner = ManifestCleaner(DIRECTORY)
        manifests_cleaner.clean_manifests()

    def test_01_sync_repository(self):
        """Measure time of synchronization."""
        for r in self.args.repositories:
            self.data.append({"remote_url": r})

        for r in self.data:
            if r["remote_url"] not in self.args.repositories:
                continue
            r["repository_name"] = utils.get_random_string()
            r["repository_href"] = create_repo(r["repository_name"])
            r["remote_name"] = utils.get_random_string()
            r["remote_href"] = create_remote(r["remote_name"], r["remote_url"])

        tasks = []
        for r in self.data:
            if r["remote_url"] not in self.args.repositories:
                continue
            task = start_sync(r["repository_href"], r["remote_href"])
            tasks.append(task)

        results = interact.wait_for_tasks(tasks)
        reporting.report_tasks_stats("Sync tasks", results)

    def test_02_resync_repository(self):
        """Measure time of resynchronization."""
        tasks = []
        for r in self.data:
            task = start_sync(r["repository_href"], r["remote_href"])
            tasks.append(task)

        results = interact.wait_for_tasks(tasks)
        reporting.report_tasks_stats("Resync tasks", results)

    def test_03_publish_repository(self):
        """Measure time of repository publishing."""
        tasks = []
        for r in self.data:
            task = create_publication(r["repository_href"])
            tasks.append(task)

        results = interact.wait_for_tasks(tasks)
        reporting.report_tasks_stats("Publication tasks", results)

        for i in range(len(results)):
            self.data[i]["publication_href"] = results[i]["created_resources"][0]
            self.data[i]["repository_version_href"] = interact.get(
                self.data[i]["publication_href"]
            )["repository_version"]

        tasks = []
        for r in self.data:
            r["distribution_name"] = utils.get_random_string()
            r["distribution_base_path"] = utils.get_random_string()
            task = create_distribution(
                r["distribution_name"], r["distribution_base_path"], r["publication_href"]
            )
            tasks.append(task)

        results = interact.wait_for_tasks(tasks)
        reporting.report_tasks_stats("Distribution tasks", results)

        for i in range(len(results)):
            self.data[i]["distribution_href"] = results[i]["created_resources"][0]
            self.data[i]["download_base_url"] = interact.get(self.data[i]["distribution_href"])[
                "base_url"
            ]

    def test_04_download_repo(self):
        """Measure time of repository downloading."""
        before = datetime.datetime.utcnow()

        for r in self.data:
            params = []
            pulp_manifest = utils.parse_pulp_manifest(r["remote_url"] + "PULP_MANIFEST")
            for f, _, s in pulp_manifest[: self.args.limit]:
                params.append((r["download_base_url"], f, s))
            with multiprocessing.Pool(processes=self.args.processes) as pool:
                pool.starmap(interact.download, params)

        after = datetime.datetime.utcnow()
        reporting.print_fmt_experiment_time("Repository download", before, after)

    def test_05_list_content(self):
        """Measure time of inspecting the repository content."""
        before = datetime.datetime.utcnow()

        durations_list = []
        for r in self.data:
            duration, content = utils.measureit(
                list_units_in_repo_ver, r["repository_version_href"]
            )
            durations_list.append(duration)

            params = []
            for c in content[: self.args.limit]:
                url = c.get("pulp_href")
                params.append((inspect_content, url))
            with multiprocessing.Pool(processes=self.args.processes) as pool:
                pool.starmap(utils.measureit, params)
        after = datetime.datetime.utcnow()
        reporting.print_fmt_experiment_time("Content inspection", before, after)

    def test_06_repo_version(self):
        """Measure time of repository cloning."""
        for r in self.data:
            r["repository_clone1_name"] = utils.get_random_string()
            r["repository_clone1_href"] = create_repo(r["repository_clone1_name"])
            r["repository_clone2_name"] = utils.get_random_string()
            r["repository_clone2_href"] = create_repo(r["repository_clone2_name"])

        tasks = []
        for r in self.data:
            task = create_repo_version_base_version(
                r["repository_clone1_href"], r["repository_version_href"]
            )
            tasks.append(task)

        results = interact.wait_for_tasks(tasks)
        reporting.report_tasks_stats("Version clone with base_version tasks", results)

        hrefs = [i["pulp_href"] for i in list_units_in_repo_ver(r["repository_version_href"])]

        tasks = []
        for r in self.data:
            task = create_repo_version_add_content_units(r["repository_clone2_href"], hrefs)
            tasks.append(task)

        results = interact.wait_for_tasks(tasks)
        reporting.report_tasks_stats("Version clone with add_content_units tasks", results)


class ManifestsDumper:
    """A handler which generates manifests in a current file system."""

    def __init__(self, directory, files_count, file_prefix, file_size):
        """Initialize all variables necessary for dumping manifest files."""
        self._directory = directory
        self._files_count = files_count
        self._file_prefix = file_prefix
        self._file_size = file_size

    def generate_manifests(self):
        """Generate manifests within specified directory."""
        pulp_manifests = []
        for i in range(FILES_COUNT):
            pulp_manifests.append(self._create_file(i))
        self._dump_manifest(pulp_manifests)

    def _create_file(self, file_id, file_suffix=".iso"):
        """Create a file with defined size and return info needed for PULP_MANIFEST."""
        file_name = self._file_prefix + str(file_id) + file_suffix
        file_path = os.path.join(self._directory, file_name)
        file_content = self._file_prefix + str(file_id).zfill(
            self._file_size - len(self._file_prefix)
        )
        file_content = file_content.encode()

        assert len(file_content) == self._file_size

        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        with open(file_path, "wb") as fp:
            fp.write(file_content)
        file_checksum = hashlib.sha256(file_content).hexdigest()

        return file_name, file_checksum, self._file_size

    def _dump_manifest(self, content):
        """Dump a PULP_MANIFEST file into a specified directory."""
        manifest_path = os.path.join(self._directory, "PULP_MANIFEST")
        with open(manifest_path, mode="w") as fp:
            writer = csv.writer(fp, delimiter=",", quoting=csv.QUOTE_NONE)
            for row in content:
                writer.writerow(row)


class ManifestCleaner:
    """A class responsible for cleaning all generated resources within the file system."""

    def __init__(self, directory):
        """Store a path to a directory which is going to be cleaned."""
        self._directory = directory

    def clean_manifests(self):
        """Remove all manifests within the directory."""
        files_pathname = os.path.join(self._directory, "*")
        for file_path in glob.glob(files_pathname):
            os.remove(file_path)


def create_repo(name):
    """Create repository"""
    return interact.post("/pulp/api/v3/repositories/file/file/", data={"name": name})["pulp_href"]


def create_remote(name, url):
    """Create remote"""
    return interact.post(
        "/pulp/api/v3/remotes/file/file/", data={"name": name, "url": url + "PULP_MANIFEST"}
    )["pulp_href"]


def start_sync(repo, remote):
    """Start sync of the remote into the repository, return task"""
    return interact.post(repo + "sync/", data={"remote": remote, "mirror": False})["task"]


def create_publication(repo):
    """Start publication of the repository, return task"""
    return interact.post("/pulp/api/v3/publications/file/file/", data={"repository": repo})["task"]


def create_distribution(name, base_path, pub):
    """Start distribution of the repository version, return task"""
    return interact.post(
        "/pulp/api/v3/distributions/file/file/",
        data={"name": name, "base_path": base_path, "publication": pub},
    )["task"]


def list_units_in_repo_ver(repo_ver):
    """List the file content with all the fields"""
    return interact.get_results(
        "/pulp/api/v3/content/file/files/", params={"repository_version": repo_ver}
    )


def inspect_content(href):
    """Inspect a file content using href"""
    return interact.get(href)


def create_repo_version_base_version(repo, ver):
    """Create repository version based on different existing version"""
    return interact.post(repo + "modify/", data={"base_version": ver})["task"]


def create_repo_version_add_content_units(repo, hrefs):
    """Create repository version based on list of hrefs"""
    return interact.post(repo + "modify/", data={"add_content_units": hrefs})["task"]
