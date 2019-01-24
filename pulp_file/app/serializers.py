from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin.serializers import (
    SingleArtifactContentSerializer,
    RemoteSerializer,
    PublisherSerializer
)

from .models import FileContent, FileRemote, FilePublisher


class FileContentSerializer(SingleArtifactContentSerializer):
    """
    Serializer for File Content.
    """

    relative_path = serializers.CharField(
        help_text="Relative location of the file within the repository"
    )

    def validate(self, data):
        """Validate the FileContent data."""
        artifact = data['_artifact']
        content = FileContent.objects.filter(digest=artifact.sha256,
                                             relative_path=data['relative_path'])

        if content.exists():
            raise serializers.ValidationError(_(
                "There is already a file content with relative path '{path}' and artifact "
                "'{artifact}'."
            ).format(path=data["relative_path"], artifact=self.initial_data["_artifact"]))

        return data

    class Meta:
        fields = SingleArtifactContentSerializer.Meta.fields + ('relative_path',)
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
