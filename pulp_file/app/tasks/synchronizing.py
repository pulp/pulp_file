import logging
import os

from gettext import gettext as _
from urllib.parse import urlparse, urlunparse

from pulpcore.plugin.models import Artifact, ProgressReport, Remote
from pulpcore.plugin.stages import (
    DeclarativeArtifact,
    DeclarativeContent,
    DeclarativeVersion,
    Stage,
)

from pulp_file.app.models import FileContent, FileRemote, FileRepository
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
    repository = FileRepository.objects.get(pk=repository_pk)

    if not remote.url:
        raise ValueError(_("A remote must have a url specified to synchronize."))

    first_stage = FileFirstStage(remote)
    dv = DeclarativeVersion(first_stage, repository, mirror=mirror)
    return dv.create()


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
        super().__init__()
        self.remote = remote

    async def run(self):
        """
        Build and emit `DeclarativeContent` from the Manifest data.
        """
        deferred_download = self.remote.policy != Remote.IMMEDIATE  # Interpret download policy
        with ProgressReport(message="Downloading Metadata", code="sync.downloading.metadata") as pb:
            parsed_url = urlparse(self.remote.url)
            root_dir = os.path.dirname(parsed_url.path)
            downloader = self.remote.get_downloader(url=self.remote.url)
            result = await downloader.run()
            pb.increment()

        with ProgressReport(message="Parsing Metadata Lines", code="sync.parsing.metadata") as pb:
            manifest = Manifest(result.path)
            entries = list(manifest.read())

            pb.total = len(entries)
            pb.save()

            for entry in entries:
                path = os.path.join(root_dir, entry.relative_path)
                url = urlunparse(parsed_url._replace(path=path))
                file = FileContent(relative_path=entry.relative_path, digest=entry.digest)
                artifact = Artifact(size=entry.size, sha256=entry.digest)
                da = DeclarativeArtifact(
                    artifact=artifact,
                    url=url,
                    relative_path=entry.relative_path,
                    remote=self.remote,
                    deferred_download=deferred_download,
                )
                dc = DeclarativeContent(content=file, d_artifacts=[da])
                pb.increment()
                await self.put(dc)
