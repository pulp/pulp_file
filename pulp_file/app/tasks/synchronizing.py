import logging
import os

from gettext import gettext as _
from urllib.parse import urlparse, urlunparse

from pulpcore.plugin.models import Artifact, ProgressBar, Repository
from pulpcore.plugin.stages import (
    DeclarativeArtifact, DeclarativeContent, DeclarativeVersion, Stage
)

from pulp_file.app.models import FileContent, FileRemote
from pulp_file.manifest import Manifest


log = logging.getLogger(__name__)


def synchronize(remote_pk, repository_pk, mirror):
    """
    Sync content from the remote repository.

    Create a new version of the repository that is synchronized with the remote.

    Args:
        remote_pk (str): The remote PK.
        repository_pk (str): The repository PK.
        mirror (bool): True for mirror mode, False for additive.

    Raises:
        ValueError: If the remote does not specify a URL to sync.

    """
    remote = FileRemote.objects.get(pk=remote_pk)
    repository = Repository.objects.get(pk=repository_pk)

    if not remote.url:
        raise ValueError(_('A remote must have a url specified to synchronize.'))

    first_stage = FileFirstStage(remote)
    DeclarativeVersion(first_stage, repository, mirror).create()


class FileFirstStage(Stage):
    """
    The first stage of a pulp_file sync pipeline.
    """

    def __init__(self, remote):
        """
        The first stage of a pulp_file sync pipeline.

        Args:
            remote (FileRemote): The remote data to be used when syncing

        """
        self.remote = remote

    async def __call__(self, in_q, out_q):
        """
        Build and emit `DeclarativeContent` from the Manifest data.

        Args:
            in_q (asyncio.Queue): Unused because the first stage doesn't read from an input queue.
            out_q (asyncio.Queue): The out_q to send `DeclarativeContent` objects to

        """
        with ProgressBar(message='Downloading Metadata') as pb:
            parsed_url = urlparse(self.remote.url)
            root_dir = os.path.dirname(parsed_url.path)
            downloader = self.remote.get_downloader(self.remote.url)
            result = await downloader.run()
            pb.increment()

        with ProgressBar(message='Parsing Metadata') as pb:
            manifest = Manifest(result.path)
            for entry in manifest.read():
                path = os.path.join(root_dir, entry.relative_path)
                url = urlunparse(parsed_url._replace(path=path))
                file = FileContent(relative_path=entry.relative_path, digest=entry.digest)
                artifact = Artifact(size=entry.size, sha256=entry.digest)
                da = DeclarativeArtifact(artifact, url, entry.relative_path, self.remote)
                dc = DeclarativeContent(content=file, d_artifacts=[da])
                pb.increment()
                await out_q.put(dc)
        await out_q.put(None)
