"""Utilities for tests for the file plugin."""
import aiohttp
import asyncio
from dataclasses import dataclass
import hashlib
import os
import requests
from tempfile import NamedTemporaryFile

from pulp_smash import api, config, utils
from pulp_smash.pulp3.constants import STATUS_PATH
from pulp_smash.pulp3.utils import gen_remote, get_content

from pulp_file.tests.functional.constants import (
    FILE_CONTENT_NAME,
    FILE_FIXTURE_MANIFEST_URL,
    FILE_URL,
)

from pulpcore.client.pulpcore import (
    ApiClient as CoreApiClient,
    ArtifactsApi,
)
from pulpcore.client.pulp_file import ApiClient as FileApiClient


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


def get_redis_status():
    """Return a boolean value which tells whether the connection to redis was established or not."""
    api_client = api.Client(config.get_config(), api.json_handler)
    status_response = api_client.get(STATUS_PATH)

    try:
        is_redis_connected = status_response["redis_connection"]["connected"]
    except (KeyError, TypeError):
        is_redis_connected = False
    return is_redis_connected


def generate_iso(full_path, size=1024, relative_path=None):
    """Generate a random file."""
    with open(full_path, "wb") as fout:
        contents = os.urandom(size)
        fout.write(contents)
        fout.flush()
    digest = hashlib.sha256(contents).hexdigest()
    if relative_path:
        name = relative_path
    else:
        name = full_path.name
    return {"name": name, "size": size, "digest": digest}


def generate_manifest(name, file_list):
    """Generate a pulp_file manifest file for a list of files."""
    with open(name, "wt") as fout:
        for file in file_list:
            fout.write("{},{},{}\n".format(file["name"], file["digest"], file["size"]))
        fout.flush()
    return name


@dataclass
class Download:
    """Class for representing a downloaded file."""

    body: bytes
    response_obj: aiohttp.ClientResponse

    def __init__(self, body, response_obj):
        self.body = body
        self.response_obj = response_obj


def get_files_in_manifest(url):
    """
    Download a File Repository manifest and return content as a list of tuples.
    [(name,sha256,size),]
    """
    files = set()
    r = asyncio.run(_download_file(url))
    for line in r.body.splitlines():
        files.add(tuple(line.decode().split(",")))
    return files


def download_file(url, auth=None, headers=None):
    """Download a file.

    :param url: str URL to the file to download
    :param auth: `aiohttp.BasicAuth` containing basic auth credentials
    :param headers: dict of headers to send with the GET request
    :return: Download
    """
    return asyncio.run(_download_file(url, auth=auth, headers=headers))


async def _download_file(url, auth=None, headers=None):
    async with aiohttp.ClientSession(auth=auth, raise_for_status=True) as session:
        async with session.get(url, verify_ssl=False, headers=headers) as response:
            return Download(body=await response.read(), response_obj=response)


def get_url(url, auth=None, headers=None):
    """
    Performs a GET request on a URL and returns an aiohttp.Response object.
    """
    return asyncio.run(_get_url(url, auth=auth, headers=headers))


async def _get_url(url, auth=None, headers=None):
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url, verify_ssl=False, headers=headers) as response:
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
