from rest_framework import serializers

from pulpcore.plugin.serializers import ContentSerializer, ImporterSerializer, PublisherSerializer

from .models import FileContent, FileImporter, FilePublisher


class FileContentSerializer(ContentSerializer):
    path = serializers.CharField()
    digest = serializers.CharField()

    class Meta:
        fields = ContentSerializer.Meta.fields + ('path', 'digest')
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
