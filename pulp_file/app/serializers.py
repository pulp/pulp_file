import copy

from rest_framework import serializers

from pulpcore.plugin.models import Artifact
from pulpcore.plugin.serializers import ContentSerializer, RemoteSerializer, PublisherSerializer

from .models import FileContent, FileRemote, FilePublisher


class FileContentSerializer(ContentSerializer):
    relative_path = serializers.CharField(
        help_text="Relative location of the file within the repository"
    )
    artifact = serializers.HyperlinkedRelatedField(
        view_name='artifacts-detail',
        help_text="Artifact file representing the physical content",
        queryset=Artifact.objects.all()
    )

    def create(self, validated_data):
        artifact = validated_data.pop('artifact')
        data = copy.deepcopy(validated_data)
        data['digest'] = artifact.sha256
        instance = FileContent.objects.create(**data)
        instance.artifact = artifact
        return instance

    class Meta:
        fields = ('_href', 'type', 'relative_path', 'artifact')
        model = FileContent


class FileRemoteSerializer(RemoteSerializer):
    class Meta:
        fields = RemoteSerializer.Meta.fields
        model = FileRemote


class FilePublisherSerializer(PublisherSerializer):
    class Meta:
        fields = PublisherSerializer.Meta.fields
        model = FilePublisher
