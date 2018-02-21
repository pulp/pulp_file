import logging
import os

from gettext import gettext as _

from celery import shared_task
from django.core.files import File

from pulpcore.plugin.models import (
    RepositoryVersion,
    Publication,
    PublishedArtifact,
    PublishedMetadata,
    RemoteArtifact,
    Repository)
from pulpcore.plugin.tasking import UserFacingTask, WorkingDirectory

from pulp_file.app.models import FileContent, FilePublisher
from pulp_file.manifest import Entry, Manifest


log = logging.getLogger(__name__)


@shared_task(base=UserFacingTask)
def publish(publisher_pk, repository_pk):
    """
    Use provided publisher to create a Publication based on a RepositoryVersion.

    Args:
        publisher_pk (str): Use the publish settings provided by this publisher.
        repository_pk (str): Create a Publication from the latest version of this Repository.
    """
    publisher = FilePublisher.objects.get(pk=publisher_pk)
    repository = Repository.objects.get(pk=repository_pk)
    repository_version = RepositoryVersion.latest(repository)

    log.info(
        _('Publishing: repository=%(repository)s, version=%(version)d, publisher=%(publisher)s'),
        {
            'repository': repository.name,
            'version': repository_version.number,
            'publisher': publisher.name,
        })

    with WorkingDirectory():
        with Publication.create(repository_version, publisher) as publication:
            manifest = Manifest('PULP_MANIFEST')
            manifest.write(populate(publication))
            metadata = PublishedMetadata(
                relative_path=os.path.basename(manifest.path),
                publication=publication,
                file=File(open(manifest.path, 'rb')))
            metadata.save()

    log.info(
        _('Publication: %(publication)s created'),
        {
            'publication': publication.pk
        })


def populate(publication):
    """
    Populate a publication.

    Create published artifacts and yield a Manifest Entry for each.

    Args:
        publication (pulpcore.plugin.models.Publication): A Publication to populate.

    Yields:
        Entry: Each manifest entry.
    """
    def find_artifact():
        _artifact = content_artifact.artifact
        if not _artifact:
            _artifact = RemoteArtifact.objects.filter(content_artifact=content_artifact).first()
        return _artifact
    paths = set()
    for content in FileContent.objects.filter(
            pk__in=publication.repository_version.content).order_by('-created'):
        if content.path in paths:
            continue
        paths.add(content.path)
        for content_artifact in content.contentartifact_set.all():
            artifact = find_artifact()
            published_artifact = PublishedArtifact(
                relative_path=content_artifact.relative_path,
                publication=publication,
                content_artifact=content_artifact)
            published_artifact.save()
            entry = Entry(
                path=content_artifact.relative_path,
                digest=artifact.sha256,
                size=artifact.size)
            yield entry
