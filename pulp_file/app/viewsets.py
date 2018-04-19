from gettext import gettext as _

from django.db import transaction
from django_filters.rest_framework import filterset
from rest_framework.decorators import detail_route
from rest_framework import serializers, status
from rest_framework.response import Response

from pulpcore.plugin.models import Artifact, Repository, RepositoryVersion
from pulpcore.plugin.viewsets import (
    ContentViewSet,
    RemoteViewSet,
    OperationPostponedResponse,
    PublisherViewSet)
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


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


class _RepositorySyncURLSerializer(serializers.Serializer):
    repository = serializers.HyperlinkedRelatedField(
        required=True,
        help_text=_('A URI of the repository to be synchronized.'),
        queryset=Repository.objects.all(),
        view_name='repositories-detail',
        label=_('Repository'),
        error_messages={
            'required': _('The repository URI must be specified.')
        })


class _RepositoryPublishURLSerializer(serializers.Serializer):

    repository = serializers.HyperlinkedRelatedField(
        help_text=_('A URI of the repository to be synchronized.'),
        required=False,
        label=_('Repository'),
        queryset=Repository.objects.all(),
        view_name='repositories-detail',
    )

    repository_version = NestedHyperlinkedRelatedField(
        help_text=_('A URI of the repository version to be published.'),
        required=False,
        label=_('Repository Version'),
        queryset=RepositoryVersion.objects.all(),
        view_name='versions-detail',
        lookup_field='number',
        parent_lookup_kwargs={'repository_pk': 'repository__pk'},
    )

    def validate(self, data):
        repository = data.get('repository')
        repository_version = data.get('repository_version')
        if (repository and not repository_version) or (not repository and repository_version):
            return data
        raise serializers.ValidationError(
            _("Either the 'repository' or 'repository_version' need to be specified "
              "but not both.")
        )


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


class FileRemoteViewSet(RemoteViewSet):
    endpoint_name = 'file'
    queryset = FileRemote.objects.all()
    serializer_class = FileRemoteSerializer

    @detail_route(methods=('post',), serializer_class=_RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Synchronizes a repository. The ``repository`` field has to be provided.
        """
        remote = self.get_object()
        serializer = _RepositorySyncURLSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        repository = serializer.validated_data.get('repository')
        result = tasks.synchronize.apply_async_with_reservation(
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

    @detail_route(methods=('post',), serializer_class=_RepositoryPublishURLSerializer)
    def publish(self, request, pk):
        """
        Publishes a repository. Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        publisher = self.get_object()
        serializer = _RepositoryPublishURLSerializer(data=request.data,
                                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get('repository_version')

        # Safe because version OR repository is enforced by serializer.
        if not repository_version:
            repository = serializer.validated_data.get('repository')
            repository_version = RepositoryVersion.latest(repository)

        result = tasks.publish.apply_async_with_reservation(
            [repository_version.repository, publisher],
            kwargs={
                'publisher_pk': str(publisher.pk),
                'repository_version_pk': str(repository_version.pk)
            }
        )
        return OperationPostponedResponse(result, request)
