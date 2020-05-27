from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin import models
from pulpcore.plugin.serializers import (
    ContentChecksumSerializer,
    DetailRelatedField,
    FilesystemExporterSerializer,
    PublicationDistributionSerializer,
    PublicationSerializer,
    RemoteSerializer,
    RepositorySerializer,
    SingleArtifactContentUploadSerializer,
)

from pulp_file.app.models import (
    FileContent,
    FileDistribution,
    FileFilesystemExporter,
    FileRemote,
    FileRepository,
    FilePublication,
)


class FileContentSerializer(SingleArtifactContentUploadSerializer, ContentChecksumSerializer):
    """
    Serializer for File Content.
    """

    def deferred_validate(self, data):
        """Validate the FileContent data."""
        data = super().deferred_validate(data)

        data["digest"] = data["artifact"].sha256

        content = FileContent.objects.filter(
            digest=data["digest"], relative_path=data["relative_path"]
        )

        if content.exists():
            raise serializers.ValidationError(
                _(
                    "There is already a file content with relative path '{path}' and digest "
                    "'{digest}'."
                ).format(path=data["relative_path"], digest=data["digest"])
            )

        return data

    class Meta:
        fields = (
            SingleArtifactContentUploadSerializer.Meta.fields
            + ContentChecksumSerializer.Meta.fields
        )
        model = FileContent


class FileRepositorySerializer(RepositorySerializer):
    """
    Serializer for File Repositories.
    """

    class Meta:
        fields = RepositorySerializer.Meta.fields
        model = FileRepository


class FileRemoteSerializer(RemoteSerializer):
    """
    Serializer for File Remotes.
    """

    policy = serializers.ChoiceField(
        help_text="The policy to use when downloading content. The possible values include: "
        "'immediate', 'on_demand', and 'streamed'. 'immediate' is the default.",
        choices=models.Remote.POLICY_CHOICES,
        default=models.Remote.IMMEDIATE,
    )

    class Meta:
        fields = RemoteSerializer.Meta.fields
        model = FileRemote


class FilePublicationSerializer(PublicationSerializer):
    """
    Serializer for File Publications.
    """

    distributions = DetailRelatedField(
        help_text=_("This publication is currently hosted as defined by these distributions."),
        source="file_filedistribution",
        view_name="filedistributions-detail",
        many=True,
        read_only=True,
    )
    manifest = serializers.CharField(
        help_text=_("Filename to use for manifest file containing metadata for all the files."),
        required=False,
        default="PULP_MANIFEST",
    )

    class Meta:
        model = FilePublication
        fields = PublicationSerializer.Meta.fields + ("distributions", "manifest")


class FileDistributionSerializer(PublicationDistributionSerializer):
    """
    Serializer for File Distributions.
    """

    class Meta:
        fields = PublicationDistributionSerializer.Meta.fields
        model = FileDistribution


class FileFilesystemExporterSerializer(FilesystemExporterSerializer):
    """
    Serializer for File file system exporters.
    """

    class Meta:
        fields = FilesystemExporterSerializer.Meta.fields
        model = FileFilesystemExporter
