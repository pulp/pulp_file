import asyncio
import logging
import os

from gettext import gettext as _
from urllib.parse import urlparse, urlunparse

from pulpcore.plugin.models import (
    Artifact, ProgressBar, RepositoryVersion, Repository
)
from pulpcore.plugin.stages import DeclarativeArtifact, DeclarativeContent, DeclarativeVersion

from pulp_file.app.models import FileContent, FileRemote
from pulp_file.manifest import Manifest


log = logging.getLogger(__name__)


def synchronize(remote_pk, repository_pk):
    """
    Create a new version of the repository that is synchronized with the remote
    as specified by the remote.

    Args:
        remote_pk (str): The remote PK.
        repository_pk (str): The repository PK.

    Raises:
        ValueError: When url is empty.
    """
    remote = FileRemote.objects.get(pk=remote_pk)
    repository = Repository.objects.get(pk=repository_pk)

    if not remote.url:
        raise ValueError(_('A remote must have a url specified to synchronize.'))

    out_q = asyncio.Queue(maxsize=100)  # restricts the number of content units in memory
    asyncio.ensure_future(fetch_manifest(remote, out_q))  # Schedule the "fetching" stage
    DeclarativeVersion(out_q, repository).create()


async def fetch_manifest(remote, out_q):
    """
    Fetch (download) the manifest.

    Args:
        remote (FileRemote): The remote data to be used when syncing
        out_q (asyncio.Queue): The out_q to send DeclarativeContent objects to
    """
    with ProgressBar(message='Downloading Metadata') as pb:
        parsed_url = urlparse(remote.url)
        root_dir = os.path.dirname(parsed_url.path)
        downloader = remote.get_downloader(remote.url)
        result = await downloader.run()
        pb.increment()

    with ProgressBar(message='Parsing Metadata') as pb:
        manifest = Manifest(result.path)
        for entry in manifest.read():
            path = os.path.join(root_dir, entry.relative_path)
            url = urlunparse(parsed_url._replace(path=path))
            file = FileContent(relative_path=entry.relative_path, digest=entry.digest)
            artifact = Artifact(size=entry.size, sha256=entry.digest)
            da = DeclarativeArtifact(artifact, url, entry.relative_path, remote)
            dc = DeclarativeContent(content=file, d_artifacts=[da])
            pb.increment()
            await out_q.put(dc)
    await out_q.put(None)
