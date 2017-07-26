from rest_framework import serializers
from pulpcore.plugin import serializers as platform

from . import models


class FileContentSerializer(platform.ContentSerializer):
    path = serializers.CharField()
    digest = serializers.CharField()

    class Meta:
        fields = platform.ContentSerializer.Meta.fields + ('path', 'digest')
        model = models.FileContent


class FileImporterSerializer(platform.ImporterSerializer):
    class Meta:
        fields = platform.ImporterSerializer.Meta.fields
        model = models.FileImporter


class BasicFileImporterSerializer(platform.ImporterSerializer):
    class Meta:
        fields = platform.ImporterSerializer.Meta.fields
        model = models.BasicFileImporter


class FilePublisherSerializer(platform.PublisherSerializer):
    class Meta:
        fields = platform.PublisherSerializer.Meta.fields
        model = models.FilePublisher
