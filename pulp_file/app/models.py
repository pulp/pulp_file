from logging import getLogger

from django.db import models

from pulpcore.plugin.models import Content, ContentArtifact, Remote, Publisher


log = getLogger(__name__)


class FileContent(Content):
    """
    The "file" content type.

    Content of this type represents a collection of 0 or more files uniquely
    identified by path and SHA256 digest.

    Fields:
        relative_path (str): The file relative path.
        digest (str): The SHA256 HEX digest.

    """
    TYPE = 'file'

    relative_path = models.TextField(blank=False, null=False)
    digest = models.TextField(blank=False, null=False)

    @property
    def artifact(self):
        return self.artifacts.get().pk

    @artifact.setter
    def artifact(self, artifact):
        if self.pk:
            ca = ContentArtifact(artifact=artifact,
                                 content=self,
                                 relative_path=self.relative_path)
            ca.save()

    class Meta:
        unique_together = (
            'relative_path',
            'digest'
        )


class FileRemote(Remote):
    """
    Remote for "file" content.
    """
    TYPE = 'file'


class FilePublisher(Publisher):
    """
    Publisher for "file" content.
    """
    TYPE = 'file'
