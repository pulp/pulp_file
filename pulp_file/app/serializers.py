from rest_framework import serializers

from pulpcore.plugin.models import Artifact
from pulpcore.plugin.serializers import ContentSerializer, ImporterSerializer, PublisherSerializer

from .models import FileContent, FileImporter, FilePublisher, FileSyncTask

from pulpcore.app.serializers.task import TaskSerializer


class FileSyncTaskSerializer(TaskSerializer):

    class Meta:
        model = FileSyncTask
        fields = ('_href', 'type')


class FileContentSerializer(ContentSerializer):
    relative_path = serializers.CharField(
        help_text="Relative location of the file within the repository"
    )
    artifact = serializers.HyperlinkedRelatedField(
        view_name='artifacts-detail',
        help_text="Artifact file representing the physical content",
        queryset=Artifact.objects.all()
    )

    class Meta:
        fields = ('_href', 'type', 'relative_path', 'artifact')
        model = FileContent


class FileImporterSerializer(ImporterSerializer):

    sync_mode = serializers.ChoiceField(
        help_text='How the importer should sync from the upstream repository.',
        allow_blank=False,
        choices=[FileImporter.MIRROR],
    )

    class Meta:
        fields = ImporterSerializer.Meta.fields
        model = FileImporter


class FilePublisherSerializer(PublisherSerializer):
    class Meta:
        fields = PublisherSerializer.Meta.fields
        model = FilePublisher
