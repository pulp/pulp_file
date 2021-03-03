# coding=utf-8
"""Utilities for tests for the file plugin."""
from functools import partial
import requests
from unittest import SkipTest
from tempfile import NamedTemporaryFile

from pulp_smash import api, config, selectors, utils
from pulp_smash.pulp3.utils import (
    gen_remote,
    gen_repo,
    get_content,
    require_pulp_3,
    require_pulp_plugins,
    sync,
)

from pulp_file.tests.functional.constants import (
    FILE_CONTENT_NAME,
    FILE_CONTENT_PATH,
    FILE_FIXTURE_MANIFEST_URL,
    FILE_PUBLICATION_PATH,
    FILE_REMOTE_PATH,
    FILE_REPO_PATH,
    FILE_URL,
)

from pulpcore.client.pulpcore import (
    ApiClient as CoreApiClient,
    ArtifactsApi,
    TasksApi,
)
from pulpcore.client.pulp_file import ApiClient as FileApiClient


cfg = config.get_config()
configuration = cfg.get_bindings_config()


def set_up_module():
    """Skip tests Pulp 3 isn't under test or if pulp-file isn't installed."""
    require_pulp_3(SkipTest)
    require_pulp_plugins({"file"}, SkipTest)


def gen_file_client():
    """Return an OBJECT for file client."""
    return FileApiClient(configuration)


def gen_file_remote(url=FILE_FIXTURE_MANIFEST_URL, **kwargs):
    """Return a semi-random dict for use in creating a file Remote.

    :param url: The URL of an external content source.
    """
    return gen_remote(url, **kwargs)


def get_file_content_paths(repo, version_href=None):
    """Return the relative path of content units present in a file repository.

    :param repo: A dict of information about the repository.
    :param version_href: The repository version to read.
    :returns: A list with the paths of units present in a given repository.
    """
    # The "relative_path" is actually a file path and name
    return [
        content_unit["relative_path"]
        for content_unit in get_content(repo, version_href)[FILE_CONTENT_NAME]
    ]


def gen_file_content_attrs(artifact):
    """Generate a dict with content unit attributes.

    :param artifact: A dict of info about the artifact.
    :returns: A semi-random dict for use in creating a content unit.
    """
    return {"artifact": artifact["pulp_href"], "relative_path": utils.uuid4()}


def gen_file_content_upload_attrs():
    """Generate a dict with content unit attributes without artifact for upload.

    :param artifact: A dict of info about the artifact.
    :returns: A semi-random dict for use in creating a content unit.
    """
    return {"relative_path": utils.uuid4()}


def populate_pulp(cfg, url=FILE_FIXTURE_MANIFEST_URL):
    """Add file contents to Pulp.

    :param pulp_smash.config.PulpSmashConfig: Information about a Pulp application.
    :param url: The URL to a file repository's ``PULP_MANIFEST`` file. Defaults to
        :data:`pulp_smash.constants.FILE_FIXTURE_MANIFEST_URL` + ``PULP_MANIFEST``.
    :returns: A list of dicts, where each dict describes one file content in Pulp.
    """
    client = api.Client(cfg, api.json_handler)
    remote = {}
    repo = {}
    try:
        remote.update(client.post(FILE_REMOTE_PATH, gen_remote(url)))
        repo.update(client.post(FILE_REPO_PATH, gen_repo()))
        sync(cfg, remote, repo)
    finally:
        if remote:
            client.delete(remote["pulp_href"])
        if repo:
            client.delete(repo["pulp_href"])
    return client.get(FILE_CONTENT_PATH)["results"]


def create_file_publication(cfg, repo, version_href=None):
    """Create a file publication.

    :param pulp_smash.config.PulpSmashConfig cfg: Information about the Pulp
        host.
    :param repo: A dict of information about the repository.
    :param version_href: A href for the repo version to be published.
    :returns: A publication. A dict of information about the just created
        publication.
    """
    if version_href:
        body = {"repository_version": version_href}
    else:
        body = {"repository": repo["pulp_href"]}

    client = api.Client(cfg, api.json_handler)
    call_report = client.post(FILE_PUBLICATION_PATH, body)
    tasks = tuple(api.poll_spawned_tasks(cfg, call_report))
    return client.get(tasks[-1]["created_resources"][0])


skip_if = partial(selectors.skip_if, exc=SkipTest)  # pylint:disable=invalid-name
"""The ``@skip_if`` decorator, customized for unittest.

:func:`pulp_smash.selectors.skip_if` is test runner agnostic. This function is
identical, except that ``exc`` has been set to ``unittest.SkipTest``.
"""

core_client = CoreApiClient(configuration)
tasks = TasksApi(core_client)


def gen_artifact(url=FILE_URL, file=None):
    """Creates an artifact."""
    if not file:
        response = requests.get(url)
        with NamedTemporaryFile() as temp_file:
            temp_file.write(response.content)
            return ArtifactsApi(core_client).create(file=temp_file.name).to_dict()

    return ArtifactsApi(core_client).create(file=file).to_dict()
