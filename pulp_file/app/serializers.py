from rest_framework import serializers

from pulpcore.plugin.models import Artifact, Repository
from pulpcore.plugin.serializers import ContentSerializer, ImporterSerializer, PublisherSerializer

from .models import FileContent, FileImporter, FilePublisher, FileSyncTask
from . import tasks

from pulpcore.app.serializers.task import TaskSerializer
from pulpcore.app.serializers.base import DetailRelatedField


class FileSyncTaskSerializer(TaskSerializer):

    importer = DetailRelatedField(
        queryset=FileImporter.objects.all()
    )
    repository = serializers.HyperlinkedRelatedField(
        view_name='repositories-detail',
        queryset=Repository.objects.all(),
    )

    reservation_structure = ["repository", "importer"]
    task_kwarg_structure = {'importer_pk': "importer.pk",
                            'repository_pk': "repository.pk"}
    celery_task = tasks.synchronize

    class Meta:
        model = FileSyncTask
        fields = TaskSerializer.Meta.fields + ("importer", "repository")


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
