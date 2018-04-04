from rest_framework import serializers

from pulpcore.plugin.models import Artifact, Repository
from pulpcore.plugin.serializers import ContentSerializer, ImporterSerializer, PublisherSerializer
from pulpcore.app.tasks import repository as core_tasks

from .models import FileContent, FileImporter, FilePublisher, FileSyncTask, FileAddRemoveTask
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


class FileAddRemoveTaskSerializer(TaskSerializer):

    repository = serializers.HyperlinkedRelatedField(
        view_name='repositories-detail',
        queryset=Repository.objects.all(),
    )

    add_content_units = DetailRelatedField(
        queryset=FileContent.objects.all(),
        many=True,
    )
    remove_content_units = DetailRelatedField(
        queryset=FileContent.objects.all(),
        many=True,
    )

    reservation_structure = ["repository"]

    # If there is custom logic related to dependencies, validation, etc, the plugin could create
    # their own task rather than using the general add/remove from pulpcore.
    celery_task = core_tasks.add_and_remove

    @property
    def task_kwargs(self):
        add_pks = [content_unit.pk for content_unit in self.task.add_content_units.all()]
        rm_pks = [content_unit.pk for content_unit in self.task.remove_content_units.all()]
        return {'repository_pk': self.task.repository.pk,
                'add_content_units': add_pks,
                'remove_content_units': rm_pks}

    # def validate(self, data):
    #     """
    #     OPTIONAL!
    #     Here, the plugin writer can provide **synchronous** validation. The plugin writer also has
    #     the opporunity to alter/clean the data.
    #
    #     Warning: The content in a repository could change between request time and task time.
    #     """
    #     for content_unit in data['add_content_units']:
    #         if content_unit in data['remove_content_units']:
    #             raise serializers.ValidationError("Cannot add and remove a single content unit")
    #     return data

    class Meta:
        model = FileAddRemoveTask
        fields = TaskSerializer.Meta.fields + ("add_content_units", "remove_content_units",
                                               "repository")


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
