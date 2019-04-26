from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin.serializers import (
    DetailRelatedField,
    PublicationSerializer,
    PublisherSerializer,
    RemoteSerializer,
    SingleArtifactContentSerializer,
    relative_path_validator,
)

from .models import FileContent, FileRemote, FilePublication, FilePublisher


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


class FilePublisherSerializer(PublisherSerializer):
    """
    Serializer for File Publishers.
    """

    manifest = serializers.CharField(
        help_text='Name of the file manifest, the full path will be url/manifest',
        required=False,
        default='PULP_MANIFEST'
    )

    class Meta:
        fields = PublisherSerializer.Meta.fields + ('manifest',)
        model = FilePublisher


class FilePublicationSerializer(PublicationSerializer):
    """
    Serializer for File Publications.
    """

    publisher = DetailRelatedField(
        help_text=_('The publisher that created this publication.'),
        queryset=FilePublisher.objects.all(),
        required=False,
    )

    class Meta:
        fields = PublicationSerializer.Meta.fields + ('publisher',)
        model = FilePublication
