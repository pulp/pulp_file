from logging import getLogger

from django.db import models

from pulpcore.plugin.models import Content, Remote, Publisher


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

    relative_path = models.TextField(null=False)
    digest = models.TextField(null=False)

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
    manifest = models.TextField()
