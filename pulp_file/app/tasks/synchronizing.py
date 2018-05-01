import logging
import os

from gettext import gettext as _
from urllib.parse import urlparse, urlunparse

from celery import shared_task

from pulpcore.plugin.models import Artifact, RepositoryVersion, Repository, ProgressSpinner
from pulpcore.plugin.changeset import (
    PendingArtifact,
    PendingContent,
    PendingVersion)
from pulpcore.plugin.tasking import UserFacingTask, WorkingDirectory

from pulp_file.app.models import FileContent, FileRemote
from pulp_file.manifest import Manifest


log = logging.getLogger(__name__)


@shared_task(base=UserFacingTask)
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
        raise ValueError(_('An remote must have a url specified to synchronize.'))

    pending_version = PendingVersion(
        pending_content_generator(remote=remote),
        repository,
        remote
    )
    pending_version.apply()
    return


def pending_content_generator(remote):
    """
    Fetch (download) the manifest and yield corresponding PendingContent units.

    Args:
        remote (FileRemote): An remote.
    """
    with ProgressSpinner(message='Parsing Metadata Entries') as spinner:
        downloader = remote.get_downloader(remote.url)
        downloader.fetch()
        manifest = Manifest(downloader.path)
        parsed_url = urlparse(remote.url)
        root_dir = os.path.dirname(parsed_url.path)
        for entry in manifest.read():
            path = os.path.join(root_dir, entry.relative_path)
            url = urlunparse(parsed_url._replace(path=path))
            file = FileContent(relative_path=entry.relative_path, digest=entry.digest)
            artifact = Artifact(size=entry.size, sha256=entry.digest)
            content = PendingContent(
                file,
                artifacts={
                    PendingArtifact(artifact, url, entry.relative_path)
                })
            spinner.done += 1
            spinner.save()
            yield content
