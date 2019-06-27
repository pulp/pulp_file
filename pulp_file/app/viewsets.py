from gettext import gettext as _  # noqa

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import detail_route

from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation
from pulpcore.plugin.viewsets import (
    BaseDistributionViewSet,
    ContentViewSet,
    ContentFilter,
    RemoteViewSet,
    OperationPostponedResponse,
    PublicationViewSet,
)

from . import tasks
from .models import FileContent, FileDistribution, FileRemote, FilePublication
from .serializers import (
    FileContentSerializer,
    FileDistributionSerializer,
    FileRemoteSerializer,
    FilePublicationSerializer,
)


class FileContentFilter(ContentFilter):
    """
    FilterSet for FileContent.
    """

    class Meta:
        model = FileContent
        fields = ["relative_path", "digest"]


class FileContentViewSet(ContentViewSet):
    """
    <!-- User-facing documentation, rendered as html-->
    FileContent represents a single file and its metadata, which can be added and removed from
    repositories.
    """

    endpoint_name = "files"
    queryset = FileContent.objects.prefetch_related("_artifacts")
    serializer_class = FileContentSerializer
    filterset_class = FileContentFilter


class FileRemoteViewSet(RemoteViewSet):
    """
    <!-- User-facing documentation, rendered as html-->
    FileRemote represents an external source of <a href="#operation/content_file_files_list">File
    Content</a>.  The target url of a FileRemote must contain a file manifest, which contains the
    metadata for all files at the source.
    """

    endpoint_name = "file"
    queryset = FileRemote.objects.all()
    serializer_class = FileRemoteSerializer

    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to sync file content.",
        responses={202: AsyncOperationResponseSerializer},
    )
    @detail_route(methods=("post",), serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Synchronizes a repository.

        The ``repository`` field has to be provided.
        """
        remote = self.get_object()
        serializer = RepositorySyncURLSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        repository = serializer.validated_data.get("repository")
        mirror = serializer.validated_data.get("mirror", False)
        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={"remote_pk": remote.pk, "repository_pk": repository.pk, "mirror": mirror},
        )
        return OperationPostponedResponse(result, request)


class FilePublicationViewSet(PublicationViewSet):
    """
    <!-- User-facing documentation, rendered as html-->
    A FilePublication contains metadata about all the <a
    href="#operation/content_file_files_list">File Content</a> in a particular <a
    href="https://docs.pulpproject.org/en/3.0/nightly/restapi.html#operation/repositories_versions_list">Repository
    Version.</a> Once a FilePublication has been created, it can be hosted using the <a
    href="#operation/distributions_file_file_list">File Distribution API.</a>
    """

    endpoint_name = "file"
    queryset = FilePublication.objects.exclude(complete=False)
    serializer_class = FilePublicationSerializer

    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to publish file content.",
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get("repository_version")
        manifest = serializer.validated_data.get("manifest")

        result = enqueue_with_reservation(
            tasks.publish,
            [repository_version.repository],
            kwargs={"repository_version_pk": str(repository_version.pk), "manifest": str(manifest)},
        )
        return OperationPostponedResponse(result, request)


class FileDistributionViewSet(BaseDistributionViewSet):
    """
    <!-- User-facing documentation, rendered as html-->
    FileDistributions host <a href="#operation/publications_file_file_list">File
    Publications</a> which makes the metadata and the referenced <a
    href="#operation/content_file_files_list">File Content</a> available to HTTP
    clients. Additionally, a FileDistribution with an associated FilePublication can be the target
    url of a <a href="#operation/remotes_file_file_list">File Remote</a> , allowing
    another instance of Pulp to sync the content.
    """

    endpoint_name = "file"
    queryset = FileDistribution.objects.all()
    serializer_class = FileDistributionSerializer
