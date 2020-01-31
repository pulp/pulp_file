import datetime
import multiprocessing

from collections import namedtuple
from unittest import TestCase

from pulp_file.tests.functional.constants import FILE_PERFORMANCE_FIXTURE_URL

from .pulpperf import interact
from .pulpperf import utils
from .pulpperf import reporting

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

        cls.args = Args(limit=100, processes=1, repositories=[FILE_PERFORMANCE_FIXTURE_URL])
        cls.data = []

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
