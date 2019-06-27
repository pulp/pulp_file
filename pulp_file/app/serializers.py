from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin import models
from pulpcore.plugin.serializers import (
    ContentChecksumSerializer,
    DetailRelatedField,
    PublicationDistributionSerializer,
    PublicationSerializer,
    RemoteSerializer,
    SingleArtifactContentSerializer,
    relative_path_validator,
)

from .models import FileContent, FileDistribution, FileRemote, FilePublication


class FileContentSerializer(SingleArtifactContentSerializer, ContentChecksumSerializer):
    """
    Serializer for File Content.
    """

    relative_path = serializers.CharField(
        help_text=_(
            "Relative location of the file within the repository. " "Example: `path/to/file.txt`"
        ),
        validators=[relative_path_validator],
    )

    def validate(self, data):
        """Validate the FileContent data."""
        data = super().validate(data)

        data["digest"] = data["_artifact"].sha256
        data["_relative_path"] = data["relative_path"]

        content = FileContent.objects.filter(
            digest=data["digest"], relative_path=data["relative_path"]
        )

        if content.exists():
            raise serializers.ValidationError(
                _(
                    "There is already a file content with relative path '{path}' and artifact "
                    "'{artifact}'."
                ).format(path=data["relative_path"], artifact=self.initial_data["_artifact"])
            )

        return data

    class Meta:
        fields = (
            tuple(set(SingleArtifactContentSerializer.Meta.fields) - {"_relative_path"})
            + ContentChecksumSerializer.Meta.fields
            + ("relative_path",)
        )
        model = FileContent


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
        source="filedistribution_set",
        many=True,
        read_only=True,
    )
    manifest = serializers.CharField(
        help_text=_("Filename to use for manifest file containing metadata for all the files."),
        write_only=True,
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
