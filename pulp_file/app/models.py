import os

from logging import getLogger

from django.db import models
from django.core.files import File
from pulpcore.plugin.models import (
    Content,
    Importer,
    Publisher,
    PublishedArtifact,
    PublishedMetadata,
    RemoteArtifact
)

from pulp_file.manifest import Manifest, Entry


log = getLogger(__name__)


class FileContent(Content):
    """
    The "file" content type.

    Content of this type represents a collection of 0 or more files uniquely
    identified by path and SHA256 digest.

    Fields:
        path (str): The file relative path.
        digest (str): The SHA256 HEX digest.

    """
    TYPE = 'file'

    path = models.TextField(blank=False, null=False)
    digest = models.TextField(blank=False, null=False)

    class Meta:
        unique_together = (
            'path',
            'digest'
        )


class FileImporter(Importer):
    """
    Importer for "file" content.
    """
    TYPE = 'file'


class FilePublisher(Publisher):
    """
    Publisher for "file" content.
    """
    TYPE = 'file'

    def publish(self):
        """
        Publish the repository.
        """
        manifest = Manifest('PULP_MANIFEST')
        manifest.write(self._publish())
        metadata = PublishedMetadata(
            relative_path=os.path.basename(manifest.path),
            publication=self.publication,
            file=File(open(manifest.path, 'rb')))
        metadata.save()

    def _publish(self):
        """
        Create published artifacts and yield the manifest entry for each.

        Yields:
            Entry: The manifest entry.
        """
        for content in self.publication.repo_version.content():
            for content_artifact in content.contentartifact_set.all():
                artifact = self._find_artifact(content_artifact)
                published_artifact = PublishedArtifact(
                    relative_path=content_artifact.relative_path,
                    publication=self.publication,
                    content_artifact=content_artifact)
                published_artifact.save()
                entry = Entry(
                    path=content_artifact.relative_path,
                    digest=artifact.sha256,
                    size=artifact.size)
                yield entry

    def _find_artifact(self, content_artifact):
        """
        Find the artifact referenced by a ContentArtifact.

        Args:
            content_artifact (pulpcore.plugin.models.ContentArtifact): A content artifact.

        Returns:
            Artifact: When the artifact exists.
            RemoteArtifact: When the artifact does not exist.
        """
        artifact = content_artifact.artifact
        if not artifact:
            artifact = RemoteArtifact.objects.get(
                content_artifact=content_artifact,
                importer__repository=self.repository)
        return artifact
