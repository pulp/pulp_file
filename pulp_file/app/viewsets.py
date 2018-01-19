from gettext import gettext as _

from django_filters.rest_framework import filterset
from pulpcore.plugin import viewsets, models as pulpcore_models
from rest_framework import decorators, serializers as drf_serializers
from rest_framework.exceptions import ValidationError

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

    @decorators.detail_route(methods=('post',))
    def publish(self, request, pk):
        request.data
        publisher_pk = str(self.get_object().pk)
        repository_pk = None
        repository_version_pk = None
        if 'repository' in request.data:
            repository_url = request.data['repository']
            repository_field = drf_serializers.HyperlinkedRelatedField(
                view_name='repositories-detail',
                queryset=pulpcore_models.Repository.objects.all(),
                source='*', initial=repository_url)
            try:
                repository_field.run_validation(data=repository_url)
                repository_pk = str(repository_field.queryset[0].pk)
            except ValidationError as e:
                # Append the URL of missing Repository to the error message
                e.detail[0] = "%s %s" % (e.detail[0], repository_url)
                raise e
        if 'repository_version' in request.data:
            repository_version_url = request.data['repository_version']
            repository_version_field = drf_serializers.HyperlinkedRelatedField(
                view_name='repository-version-detail',
                queryset=pulpcore_models.Repository.objects.all(),
                source='*', initial=repository_version_url)
            try:
                repository_version_field.run_validation(data=repository_version_url)
                repository_version_pk = str(repository_field.queryset[0].pk)
            except ValidationError as e:
                # Append the URL of missing Repository to the error message
                e.detail[0] = "%s %s" % (e.detail[0], repository_version_url)
                raise e
        async_result = tasks.publish.apply_async_with_reservation(
            viewsets.tags.RESOURCE_REPOSITORY_TYPE, repository_pk,
            kwargs={'publisher_pk': publisher_pk,
                    'repository_pk': repository_pk,
                    'repository_version_pk': repository_version_pk}
        )
        return viewsets.OperationPostponedResponse([async_result], request)