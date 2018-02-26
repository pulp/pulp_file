from logging import getLogger

from django.db import models

from pulpcore.plugin.models import Content, Importer, Publisher


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
