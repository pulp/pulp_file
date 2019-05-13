from logging import getLogger

from django.db import models

from pulpcore.plugin.models import Content, PublicationDistribution, Remote, Publication


log = getLogger(__name__)


class FileContent(Content):
    """
    The "file" content type.

    Content of this type represents a single file uniquely
    identified by path and SHA256 digest.

    Fields:
        relative_path (str): The file relative path.
        digest (str): The SHA256 HEX digest.
    """

    TYPE = 'file'

    relative_path = models.CharField(max_length=255, null=False)
    digest = models.CharField(max_length=64, null=False)

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


class FilePublication(Publication):
    """
    Publication for 'file' content.
    """

    TYPE = 'file'


class FileDistribution(PublicationDistribution):
    """
    Distribution for 'file' content.
    """

    TYPE = 'file'
