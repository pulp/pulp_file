from gettext import gettext as _

from django.db import transaction
from django_filters.rest_framework import filterset
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import detail_route
from rest_framework import serializers, status
from rest_framework.response import Response

from pulpcore.plugin.models import Artifact
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositoryPublishURLSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation
from pulpcore.plugin.viewsets import (
    ContentViewSet,
    RemoteViewSet,
    OperationPostponedResponse,
    PublisherViewSet)

from . import tasks
from .models import FileContent, FileRemote, FilePublisher
from .serializers import FileContentSerializer, FileRemoteSerializer, FilePublisherSerializer


class FileContentFilter(filterset.FilterSet):
    class Meta:
        model = FileContent
        fields = [
            'relative_path',
            'digest'
        ]


class FileContentViewSet(ContentViewSet):
    endpoint_name = 'file/files'
    queryset = FileContent.objects.all()
    serializer_class = FileContentSerializer
    filterset_class = FileContentFilter

    @transaction.atomic
    def create(self, request):
        try:
            artifact = self.get_resource(request.data['artifact'], Artifact)
        except KeyError:
            raise serializers.ValidationError(detail={'artifact': _('This field is required')})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.save(digest=artifact.sha256)
        content.artifact = artifact

        headers = self.get_success_headers(request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FileRemoteViewSet(RemoteViewSet):
    endpoint_name = 'file'
    queryset = FileRemote.objects.all()
    serializer_class = FileRemoteSerializer

    @swagger_auto_schema(operation_description="Trigger an asynchronous task to sync file "
                                               "content.",
                         responses={202: AsyncOperationResponseSerializer})
    @detail_route(methods=('post',), serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Synchronizes a repository. The ``repository`` field has to be provided.
        """
        remote = self.get_object()
        serializer = RepositorySyncURLSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        repository = serializer.validated_data.get('repository')
        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={
                'remote_pk': remote.pk,
                'repository_pk': repository.pk
            }
        )
        return OperationPostponedResponse(result, request)


class FilePublisherViewSet(PublisherViewSet):
    endpoint_name = 'file'
    queryset = FilePublisher.objects.all()
    serializer_class = FilePublisherSerializer

    @swagger_auto_schema(operation_description="Trigger an asynchronous task to publish "
                                               "R content.",
                         responses={202: AsyncOperationResponseSerializer})
    @detail_route(methods=('post',), serializer_class=RepositoryPublishURLSerializer)
    def publish(self, request, pk):
        """
        Publishes a repository. Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        publisher = self.get_object()
        serializer = RepositoryPublishURLSerializer(data=request.data,
                                                    context={'request': request})
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get('repository_version')

        result = enqueue_with_reservation(
            tasks.publish,
            [repository_version.repository, publisher],
            kwargs={
                'publisher_pk': str(publisher.pk),
                'repository_version_pk': str(repository_version.pk)
            }
        )
        return OperationPostponedResponse(result, request)
