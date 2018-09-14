from rest_framework import serializers

from pulpcore.plugin.models import Artifact
from pulpcore.plugin.serializers import (
    ContentSerializer,
    RelatedField,
    RemoteSerializer,
    PublisherSerializer
)

from .models import FileContent, FileRemote, FilePublisher


class FileContentSerializer(ContentSerializer):
    """
    Serializer for File Content.
    """

    relative_path = serializers.CharField(
        help_text="Relative location of the file within the repository"
    )
    artifact = RelatedField(
        view_name='artifacts-detail',
        help_text="Artifact file representing the physical content",
        queryset=Artifact.objects.all()
    )

    class Meta:
        fields = tuple(set(ContentSerializer.Meta.fields) - {'artifacts'}) + ('relative_path',
                                                                              'artifact')
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
