from django.db import models

from pulp.plugin import models as platform


class FileContent(platform.Content):
    """
    The "file" content type.

    Content of this type represents a collection of 0 or more files identified by a unique name.

    Fields:
        name (str): A unique name for this content.

    """
    TYPE = 'file'

    name = models.TextField(unique=True, null=False)

    natural_key_fields = (name,)


class FileImporter(platform.Importer):
    """
    Importer for "file" content.
    """
    TYPE = 'file'

    def sync(self):
        """
        Perform a sync.

        Sync behavior for the file plugin has not yet been implemented.
        """
        raise NotImplementedError


class FilePublisher(platform.Publisher):
    """
    Publisher for "file" content.
    """
    TYPE = 'file'

    def publish(self):
        """
        Perform a publish.

        Publish behavior for the file plugin has not yet been implemented.
        """
        raise NotImplementedError
