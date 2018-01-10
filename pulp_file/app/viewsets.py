from gettext import gettext as _

from django_filters.rest_framework import filterset
from pulpcore.plugin import viewsets
from rest_framework import decorators

from . import models, serializers, tasks


class FileContentFilter(filterset.FilterSet):
    class Meta:
        model = models.FileContent
        fields = ['path', 'digest']


class FileContentViewSet(viewsets.ContentViewSet):
    endpoint_name = 'file'
    queryset = models.FileContent.objects.all()
    serializer_class = serializers.FileContentSerializer
    filter_class = FileContentFilter


class FileImporterViewSet(viewsets.ImporterViewSet):
    endpoint_name = 'file'
    queryset = models.FileImporter.objects.all()
    serializer_class = serializers.FileImporterSerializer

    @decorators.detail_route(methods=('post',))
    def sync(self, request, pk):
        importer = self.get_object()
        if not importer.feed_url:
            # TODO(asmacdo) make sure this raises a 400
            raise ValueError(_("An importer must have a 'feed_url' attribute to sync."))

        async_result = tasks.sync.apply_async_with_reservation(
            viewsets.tags.RESOURCE_REPOSITORY_TYPE, str(importer.repository.pk),
            kwargs={'importer_pk': importer.pk}
        )
        return viewsets.OperationPostponedResponse([async_result], request)


class FilePublisherViewSet(viewsets.PublisherViewSet):
    endpoint_name = 'file'
    queryset = models.FilePublisher.objects.all()
    serializer_class = serializers.FilePublisherSerializer
