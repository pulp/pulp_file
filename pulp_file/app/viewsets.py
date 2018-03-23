from gettext import gettext as _

from django.db import transaction
from django_filters.rest_framework import filterset
from rest_framework.decorators import detail_route
from rest_framework import mixins, serializers, status
from rest_framework.response import Response

from pulpcore.plugin.models import Artifact, Repository, RepositoryVersion

from pulpcore.plugin.viewsets import (
    ContentViewSet,
    ImporterViewSet,
    OperationPostponedResponse,
    PublisherViewSet)

from . import tasks
from .models import FileContent, FileImporter, FilePublisher, FileSyncTask, FileTask
from .serializers import FileContentSerializer, FileImporterSerializer, FilePublisherSerializer
from .serializers import FileSyncTaskSerializer

from pulpcore.app.viewsets.task import TaskViewSet


class FileTaskViewSet(TaskViewSet):

    endpoint_name = 'file'
    queryset = FileTask.objects.all()
    model = FileTask


class FileSyncTaskViewSet(TaskViewSet, mixins.CreateModelMixin):

    endpoint_name = 'file/syncs'
    queryset = FileSyncTask.objects.all()
    model = FileSyncTask
    serializer_class = FileSyncTaskSerializer


class FileContentFilter(filterset.FilterSet):
    class Meta:
        model = FileContent
        fields = [
            'relative_path',
            'digest'
        ]


class FileContentViewSet(ContentViewSet):
    endpoint_name = 'file'
    queryset = FileContent.objects.all()
    serializer_class = FileContentSerializer
    filter_class = FileContentFilter

    @transaction.atomic
    def create(self, request):
        try:
            artifact = self.get_resource(request.data['artifact'], Artifact)
        except KeyError:
            raise serializers.ValidationError(detail={'artifact': _('This field is required')})

        data = request.data
        data['digest'] = artifact.sha256
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        content = serializer.save()
        content.artifact = artifact

        headers = self.get_success_headers(request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FileImporterViewSet(ImporterViewSet):
    endpoint_name = 'file'
    queryset = FileImporter.objects.all()
    serializer_class = FileImporterSerializer


class FilePublisherViewSet(PublisherViewSet):
    endpoint_name = 'file'
    queryset = FilePublisher.objects.all()
    serializer_class = FilePublisherSerializer

    @detail_route(methods=('post',))
    def publish(self, request, pk):
        publisher = self.get_object()
        repository = None
        repository_version = None
        if 'repository' not in request.data and 'repository_version' not in request.data:
            raise serializers.ValidationError(_("Either the 'repository' or 'repository_version' "
                                              "need to be specified."))

        if 'repository' in request.data and request.data['repository']:
            repository = self.get_resource(request.data['repository'], Repository)

        if 'repository_version' in request.data and request.data['repository_version']:
            repository_version = self.get_resource(request.data['repository_version'],
                                                   RepositoryVersion)

        if repository and repository_version:
            raise serializers.ValidationError(_("Either the 'repository' or 'repository_version' "
                                              "can be specified - not both."))

        if not repository_version:
            repository_version = RepositoryVersion.latest(repository)

        result = tasks.publish.apply_async_with_reservation(
            [repository_version.repository, publisher],
            kwargs={
                'publisher_pk': str(publisher.pk),
                'repository_version_pk': str(repository_version.pk)
            }
        )
        return OperationPostponedResponse([result], request)
