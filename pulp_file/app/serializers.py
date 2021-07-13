from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin import models
from pulpcore.plugin.serializers import (
    AlternateContentSourceSerializer,
    ContentChecksumSerializer,
    DetailRelatedField,
    DistributionSerializer,
    PublicationSerializer,
    RemoteSerializer,
    RepositorySerializer,
    SingleArtifactContentUploadSerializer,
)

from pulp_file.app.models import (
    FileAlternateContentSource,
    FileContent,
    FileDistribution,
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
            content.get().touch()

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

    autopublish = serializers.BooleanField(
        help_text=_(
            "Whether to automatically create publications for new repository versions, "
            "and update any distributions pointing to this repository."
        ),
        default=False,
        required=False,
    )

    manifest = serializers.CharField(
        help_text=_("Filename to use for manifest file containing metadata for all the files."),
        default="PULP_MANIFEST",
        required=False,
    )

    class Meta:
        fields = RepositorySerializer.Meta.fields + ("autopublish", "manifest")
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
        source="distribution_set",
        view_name="filedistributions-detail",
        many=True,
        read_only=True,
    )
    manifest = serializers.CharField(
        help_text=_("Filename to use for manifest file containing metadata for all the files."),
        default="PULP_MANIFEST",
        required=False,
    )

    class Meta:
        model = FilePublication
        fields = PublicationSerializer.Meta.fields + ("distributions", "manifest")


class FileDistributionSerializer(DistributionSerializer):
    """
    Serializer for File Distributions.
    """

    publication = DetailRelatedField(
        required=False,
        help_text=_("Publication to be served"),
        view_name_pattern=r"publications(-.*/.*)?-detail",
        queryset=models.Publication.objects.exclude(complete=False),
        allow_null=True,
    )

    def validate(self, data):
        """
        Ensure publication and repository are not set at the same time.

        This is needed here till https://pulp.plan.io/issues/8761 is resolved.
        """
        data = super().validate(data)
        repository_provided = data.get("repository", None)
        publication_provided = data.get("publication", None)

        if repository_provided and publication_provided:
            raise serializers.ValidationError(
                _(
                    "Only one of the attributes 'repository' and 'publication' "
                    "may be used simultaneously."
                )
            )
        if repository_provided or publication_provided:
            data["repository"] = repository_provided
            data["publication"] = publication_provided
        return data

    class Meta:
        fields = DistributionSerializer.Meta.fields + ("publication",)
        model = FileDistribution


class FileAlternateContentSourceSerializer(AlternateContentSourceSerializer):
    """
    Serializer for File alternate content source.
    """

    class Meta:
        fields = AlternateContentSourceSerializer.Meta.fields
        model = FileAlternateContentSource
