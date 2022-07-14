"""Utilities for tests for the file plugin."""
import aiohttp
import asyncio
from datetime import datetime
from functools import partial
import hashlib
import os
import requests
from unittest import SkipTest
from tempfile import NamedTemporaryFile

from pulp_smash import api, cli, config, selectors, utils
from pulp_smash.pulp3.bindings import monitor_task
from pulp_smash.pulp3.constants import STATUS_PATH
from pulp_smash.pulp3.utils import (
    gen_remote,
    gen_repo,
    get_content,
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
    ExportersPulpApi,
    UsersApi,
    UsersRolesApi,
)
from pulpcore.client.pulp_file import ApiClient as FileApiClient
from pulpcore.client.pulp_file import DistributionsFileApi


cfg = config.get_config()
configuration = cfg.get_bindings_config()


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


skip_if = partial(selectors.skip_if, exc=SkipTest)  # pylint:disable=invalid-name
"""The ``@skip_if`` decorator, customized for unittest.

:func:`pulp_smash.selectors.skip_if` is test runner agnostic. This function is
identical, except that ``exc`` has been set to ``unittest.SkipTest``.
"""


def gen_artifact(url=FILE_URL, file=None):
    """Creates an artifact."""
    core_client = gen_pulpcore_client()
    if not file:
        response = requests.get(url)
        with NamedTemporaryFile() as temp_file:
            temp_file.write(response.content)
            temp_file.flush()
            return ArtifactsApi(core_client).create(file=temp_file.name).to_dict()

    return ArtifactsApi(core_client).create(file=file).to_dict()


def gen_pulpcore_client():
    """Return an OBJECT for pulpcore client."""
    configuration = config.get_config().get_bindings_config()
    return CoreApiClient(configuration)


def gen_file_client():
    """Return an OBJECT for file client."""
    configuration = config.get_config().get_bindings_config()
    return FileApiClient(configuration)


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
    return api.Client(cfg).post(FILE_PUBLICATION_PATH, body)


def create_repo_and_versions(syncd_repo, repo_api, versions_api, content_api):
    """Create a repo with multiple versions.

    :param syncd_repo: A Repository that has at least three Content-units for us to copy from.
    :param pulpcore.client.pulp_file.RepositoriesFileApi repo_api: client to talk to the Repository
        API
    :param pulpcore.client.pulp_file.RepositoriesFileVersionsApi versions_api: client to talk to
        the RepositoryVersions API
    :param pulpcore.client.pulp_file.ContentFilesApi content_api: client to talk to the Content API
    :returns: A (FileRepository, [FileRepositoryVersion...]) tuple
    """
    # Create a new file-repo
    a_repo = repo_api.create(gen_repo())
    # get a list of all the files from one of our existing repos
    file_list = content_api.list(repository_version=syncd_repo.latest_version_href)
    # copy files from repositories[0] into new, one file at a time
    results = file_list.results
    for a_file in results:
        href = a_file.pulp_href
        modify_response = repo_api.modify(a_repo.pulp_href, {"add_content_units": [href]})
        monitor_task(modify_response.task)
    # get all versions of that repo
    versions = versions_api.list(a_repo.pulp_href, ordering=["number"])
    return a_repo, versions


def delete_exporter(exporter):
    """
    Utility routine to delete an exporter and any exported files
    :param exporter : PulpExporter to delete
    """
    cfg = config.get_config()
    cli_client = cli.Client(cfg)
    core_client = CoreApiClient(configuration=cfg.get_bindings_config())
    exporter_api = ExportersPulpApi(core_client)
    cmd = ("rm", "-rf", exporter.path)

    cli_client.run(cmd, sudo=True)
    result = exporter_api.delete(exporter.pulp_href)
    monitor_task(result.task)


def create_distribution(repository_href=None):
    """Utility to create a pulp_file distribution."""
    file_client = gen_file_client()
    distro_api = DistributionsFileApi(file_client)

    body = {"name": utils.uuid4(), "base_path": utils.uuid4()}
    if repository_href:
        body["repository"] = repository_href

    result = distro_api.create(body)
    distro_href = monitor_task(result.task).created_resources[0]
    distro = distro_api.read(distro_href)
    return distro


def gen_user_rest(cfg=None, model_roles=None, object_roles=None, **kwargs):
    """Add a user with a set of roles using the REST API."""
    if cfg is None:
        cfg = config.get_config()
    api_config = cfg.get_bindings_config()
    admin_core_client = CoreApiClient(api_config)
    admin_user_api = UsersApi(admin_core_client)
    admin_user_roles_api = UsersRolesApi(admin_core_client)

    user_body = {
        "username": utils.uuid4(),
        "password": utils.uuid4(),
    }
    user_body.update(kwargs)

    user = admin_user_api.create(user_body)

    if model_roles:
        for role in model_roles:
            user_role = {"role": role, "content_object": None}
            admin_user_roles_api.create(user.pulp_href, user_role)
    if object_roles:
        for role, obj in object_roles:
            user_role = {"role": role, "content_object": obj}
            admin_user_roles_api.create(user.pulp_href, user_role)

    user_body.update(user.to_dict())
    return user_body


def del_user_rest(user_href, cfg=None):
    """Delete a user using the REST API."""
    if cfg is None:
        cfg = config.get_config()
    api_config = cfg.get_bindings_config()
    admin_core_client = CoreApiClient(api_config)
    admin_user_api = UsersApi(admin_core_client)

    admin_user_api.delete(user_href)


def get_redis_status():
    """Return a boolean value which tells whether the connection to redis was established or not."""
    api_client = api.Client(config.get_config(), api.json_handler)
    status_response = api_client.get(STATUS_PATH)

    try:
        is_redis_connected = status_response["redis_connection"]["connected"]
    except (KeyError, TypeError):
        is_redis_connected = False
    return is_redis_connected


def parse_date_from_string(s, parse_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    """Parse string to datetime object.

    :param s: str like '2018-11-18T21:03:32.493697Z'
    :param parse_format: str defaults to %Y-%m-%dT%H:%M:%S.%fZ
    :return: datetime.datetime
    """
    return datetime.strptime(s, parse_format)


def generate_iso(name, size=1024):
    """Generate a random file."""
    with open(name, "wb") as fout:
        contents = os.urandom(size)
        fout.write(contents)
        fout.flush()
    digest = hashlib.sha256(contents).hexdigest()
    return {"name": name.name, "size": size, "digest": digest}


def generate_manifest(name, file_list):
    """Generate a pulp_file manifest file for a list of files."""
    with open(name, "wt") as fout:
        for file in file_list:
            fout.write("{},{},{}\n".format(file["name"], file["digest"], file["size"]))
        fout.flush()
    return name


def get_files_in_manifest(url):
    """
    Download a File Repository manifest and return content as a list of tuples.
    [(name,sha256,size),]
    """
    files = set()
    r = asyncio.run(_download_file(url))
    for line in r.splitlines():
        files.add(tuple(line.decode().split(",")))
    return files


def download_file(url, auth=None):
    """
    Performs a GET request on a URL.
    """
    return asyncio.run(_download_file(url, auth=auth))


async def _download_file(url, auth=None):
    async with aiohttp.ClientSession(auth=auth, raise_for_status=True) as session:
        async with session.get(url, verify_ssl=False) as response:
            return await response.read()


def get_url(url, auth=None):
    """
    Performs a GET request on a URL and returns an aiohttp.Response object.
    """
    return asyncio.run(_get_url(url, auth=auth))


async def _get_url(url, auth=None):
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url, verify_ssl=False) as response:
            return response


def post_url(url, data=None, auth=None, return_body=False):
    """Performs a POST request on a URL and returns an aiohttp.Response object."""
    return asyncio.run(_post_url(url, data, return_body, auth=auth))


async def _post_url(url, data, return_body, auth=None):
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, data=data, verify_ssl=False) as response:
            if return_body:
                return await response.read()
            return response
