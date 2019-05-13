from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin.serializers import (
    DetailRelatedField,
    PublicationDistributionSerializer,
    PublicationSerializer,
    RemoteSerializer,
    SingleArtifactContentSerializer,
    relative_path_validator,
)

from .models import FileContent, FileDistribution, FileRemote, FilePublication


class FileContentSerializer(SingleArtifactContentSerializer):
    """
    Serializer for File Content.
    """

    relative_path = serializers.CharField(
        help_text=_("Relative location of the file within the repository"),
        validators=[relative_path_validator],
    )

    def validate(self, data):
        """Validate the FileContent data."""
        data = super().validate(data)

        data['digest'] = data['_artifact'].sha256
        data['_relative_path'] = data['relative_path']

        content = FileContent.objects.filter(digest=data['digest'],
                                             relative_path=data['relative_path'])

        if content.exists():
            raise serializers.ValidationError(_(
                "There is already a file content with relative path '{path}' and artifact "
                "'{artifact}'."
            ).format(path=data["relative_path"], artifact=self.initial_data["_artifact"]))

        return data

    class Meta:
        fields = tuple(
            set(SingleArtifactContentSerializer.Meta.fields) - {'_relative_path'}
        ) + ('relative_path',)
        model = FileContent


class FileRemoteSerializer(RemoteSerializer):
    """
    Serializer for File Remotes.
    """

    class Meta:
        fields = RemoteSerializer.Meta.fields
        model = FileRemote


class FilePublicationSerializer(PublicationSerializer):
    """
    Serializer for File Publications.
    """

    distributions = DetailRelatedField(
        help_text=_('This publication is currently being served as '
                    'defined by these distributions.'),
        source="filedistribution_set",
        many=True,
        read_only=True,
    )
    manifest = serializers.CharField(
        help_text=_("Filename to use for manifest file. Default is 'PULP_MANIFEST'."),
        write_only=True,
        required=False,
        default='PULP_MANIFEST',
    )

    class Meta:
        model = FilePublication
        fields = PublicationSerializer.Meta.fields + (
            'distributions',
            'manifest',
        )


class FileDistributionSerializer(PublicationDistributionSerializer):
    """
    Serializer for File Distributions.
    """

    class Meta:
        fields = PublicationDistributionSerializer.Meta.fields
        model = FileDistribution
