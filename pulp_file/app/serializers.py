from rest_framework import serializers
from pulp.plugin import serializers as platform

from . import models


class FileContentSerializer(platform.ContentSerializer):
    name = serializers.CharField()

    class Meta:
        fields = platform.ContentSerializer.Meta.fields + ('name',)
        model = models.FileContent


class FileImporterSerializer(platform.ImporterSerializer):
    class Meta:
        fields = platform.ImporterSerializer.Meta.fields
        model = models.FileImporter


class FilePublisherSerializer(platform.PublisherSerializer):
    class Meta:
        fields = platform.PublisherSerializer.Meta.fields
        model = models.FilePublisher
