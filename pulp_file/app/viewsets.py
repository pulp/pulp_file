from django_filters.rest_framework import filterset
from pulpcore.plugin import viewsets as platform

from . import models, serializers


class FileContentFilter(filterset.FilterSet):
    class Meta:
        model = models.FileContent
        fields = ['path', 'digest']


class FileContentViewSet(platform.ContentViewSet):
    endpoint_name = 'file'
    queryset = models.FileContent.objects.all()
    serializer_class = serializers.FileContentSerializer
    filter_class = FileContentFilter


class FileImporterViewSet(platform.ImporterViewSet):
    endpoint_name = 'file'
    queryset = models.FileImporter.objects.all()
    serializer_class = serializers.FileImporterSerializer


class BasicFileImporterViewSet(platform.ImporterViewSet):
    endpoint_name = 'basicfile'
    queryset = models.BasicFileImporter.objects.all()
    serializer_class = serializers.BasicFileImporterSerializer


class FilePublisherViewSet(platform.PublisherViewSet):
    endpoint_name = 'file'
    queryset = models.FilePublisher.objects.all()
    serializer_class = serializers.FilePublisherSerializer
