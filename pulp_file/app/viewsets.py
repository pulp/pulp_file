from gettext import gettext as _

from django_filters.rest_framework import filterset
from rest_framework.compat import coreapi, coreschema
from rest_framework.decorators import detail_route
from rest_framework.schemas import ManualSchema
from rest_framework import serializers


from pulpcore.plugin.models import Repository
from pulpcore.plugin.viewsets import (
    ContentViewSet,
    ImporterViewSet,
    OperationPostponedResponse,
    PublisherViewSet)

from . import tasks
from .models import FileContent, FileImporter, FilePublisher
from .serializers import FileContentSerializer, FileImporterSerializer, FilePublisherSerializer


class FileContentFilter(filterset.FilterSet):
    class Meta:
        model = FileContent
        fields = [
            'path',
            'digest'
        ]


class FileContentViewSet(ContentViewSet):
    endpoint_name = 'file'
    queryset = FileContent.objects.all()
    serializer_class = FileContentSerializer
    filter_class = FileContentFilter


class FileImporterViewSet(ImporterViewSet):
    endpoint_name = 'file'
    queryset = FileImporter.objects.all()
    serializer_class = FileImporterSerializer

    @detail_route(
        methods=('post',),
        schema=ManualSchema(
            fields=[
                coreapi.Field(
                    name='repository',
                    schema=coreschema.String(
                        description=_('URI for the repository to be synchronized.')),
                    required=True)
            ]))
    def sync(self, request, pk):
        importer = self.get_object()
        try:
            repository_uri = request.data['repository']
        except KeyError:
            raise serializers.ValidationError(detail=_('Repository URI must be specified.'))
        if not importer.feed_url:
            raise serializers.ValidationError(detail=_('A feed_url must be specified.'))
        repository = self.get_resource(repository_uri, Repository)
        result = tasks.synchronize.apply_async_with_reservation(
            [repository, importer],
            kwargs={
                'importer_pk': importer.pk,
                'repository_pk': repository.pk
            }
        )
        return OperationPostponedResponse([result], request)


class FilePublisherViewSet(PublisherViewSet):
    endpoint_name = 'file'
    queryset = FilePublisher.objects.all()
    serializer_class = FilePublisherSerializer

    @detail_route(
        methods=('post',),
        schema=ManualSchema(
            fields=[
                coreapi.Field(
                    name='repository',
                    schema=coreschema.String(
                        description=_('URI for the repository to be published.')),
                    required=True)
            ]))
    def publish(self, request, pk):
        try:
            repository_uri = request.data['repository']
        except KeyError:
            raise serializers.ValidationError(detail=_('Repository URI must be specified.'))
        publisher = self.get_object()
        repository = self.get_resource(repository_uri, Repository)
        result = tasks.publish.apply_async_with_reservation(
            [repository, publisher],
            kwargs={
                'publisher_pk': str(publisher.pk),
                'repository_pk': repository.pk
            }
        )
        return OperationPostponedResponse([result], request)
