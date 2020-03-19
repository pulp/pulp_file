from logging import getLogger

from django.db import models

from pulpcore.plugin.models import (
    Content,
    FileSystemExporter,
    Publication,
    PublicationDistribution,
    Remote,
    Repository,
)
from pulpcore.plugin.publication_utils import validate_publication_paths
from pulpcore.plugin.repo_version_utils import remove_duplicates, validate_repo_version


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

    TYPE = "file"
    repo_key_fields = ("relative_path",)

    relative_path = models.TextField(null=False)
    digest = models.CharField(max_length=64, null=False)

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"
        unique_together = ("relative_path", "digest")


class FileRepository(Repository):
    """
    The "file" repository type.
    """

    TYPE = "file"
    CONTENT_TYPES = [FileContent]

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"

    def finalize_new_version(self, new_version):
        """
        Finalize and validate the new repository version.

        Ensure no added content contains the same `relative_path` as other content and relative
        paths don't overlap.

        Args:
            new_version (pulpcore.app.models.RepositoryVersion): The incomplete RepositoryVersion to
                finalize.

        """
        remove_duplicates(new_version)
        validate_repo_version(new_version)


class FileRemote(Remote):
    """
    Remote for "file" content.
    """

    TYPE = "file"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class FilePublication(Publication):
    """
    Publication for 'file' content.
    """

    TYPE = "file"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"

    def finalize_new_publication(self):
        """
        Validate that artifact paths don't overlap.
        """
        validate_publication_paths(self)


class FileDistribution(PublicationDistribution):
    """
    Distribution for 'file' content.
    """

    TYPE = "file"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class FileFileSystemExporter(FileSystemExporter):
    """
    File system exporter for 'file' content.
    """

    TYPE = "filesystem"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"
