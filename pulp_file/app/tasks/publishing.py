import logging

from gettext import gettext as _

from django.core.files import File

from pulpcore.plugin.models import RepositoryVersion, PublishedMetadata, RemoteArtifact
from pulpcore.plugin.tasking import WorkingDirectory

from pulp_file.app.models import FileContent, FilePublication
from pulp_file.manifest import Entry, Manifest


log = logging.getLogger(__name__)


def publish(manifest, repository_version_pk):
    """
    Create a Publication based on a RepositoryVersion.

    Args:
        manifest (str): Filename to use for manifest file.
        repository_version_pk (str): Create a publication from this repository version.

    """
    repo_version = RepositoryVersion.objects.get(pk=repository_version_pk)

    log.info(
        _("Publishing: repository={repo}, version={ver}, manifest={manifest}").format(
            repo=repo_version.repository.name, ver=repo_version.number, manifest=manifest
        )
    )

    with WorkingDirectory():
        with FilePublication.create(repo_version, pass_through=True) as publication:
            manifest = Manifest(manifest)
            manifest.write(populate(publication))
            PublishedMetadata.create_from_file(
                file=File(open(manifest.relative_path, "rb")), publication=publication
            )

    log.info(_("Publication: {publication} created").format(publication=publication.pk))


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

    for content in FileContent.objects.filter(
        pk__in=publication.repository_version.content
    ).order_by("-pulp_created"):
        for content_artifact in content.contentartifact_set.all():
            artifact = find_artifact()
            entry = Entry(
                relative_path=content_artifact.relative_path,
                digest=artifact.sha256,
                size=artifact.size,
            )
            yield entry
