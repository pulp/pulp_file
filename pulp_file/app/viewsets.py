from django.http import Http404
from django_filters import CharFilter
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from pulpcore.plugin.actions import ModifyRepositoryActionMixin
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    PublicationExportSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation, fs_publication_export
from pulpcore.plugin.viewsets import (
    BaseDistributionViewSet,
    ContentFilter,
    ExporterViewSet,
    ExportViewSet,
    OperationPostponedResponse,
    PublicationViewSet,
    RemoteViewSet,
    RepositoryViewSet,
    RepositoryVersionViewSet,
    SingleArtifactContentUploadViewSet,
)

from . import tasks
from .models import (
    FileContent,
    FileDistribution,
    FileFilesystemExporter,
    FileRemote,
    FileRepository,
    FilePublication,
)
from .serializers import (
    FileContentSerializer,
    FileDistributionSerializer,
    FileFilesystemExporterSerializer,
    FileRemoteSerializer,
    FileRepositorySerializer,
    FilePublicationSerializer,
)


class FileContentFilter(ContentFilter):
    """
    FilterSet for FileContent.
    """

    sha256 = CharFilter(field_name="_artifacts__sha256")

    class Meta:
        model = FileContent
        fields = ["relative_path", "sha256"]


class FileContentViewSet(SingleArtifactContentUploadViewSet):
    """
    <!-- User-facing documentation, rendered as html-->
    FileContent represents a single file and its metadata, which can be added and removed from
    repositories.
    """

    endpoint_name = "files"
    queryset = FileContent.objects.prefetch_related("_artifacts")
    serializer_class = FileContentSerializer
    filterset_class = FileContentFilter


class FileRepositoryViewSet(RepositoryViewSet, ModifyRepositoryActionMixin):
    """
    <!-- User-facing documentation, rendered as html-->
    FileRepository represents a single file repository, to which content can be synced, added,
    or removed.
    """

    endpoint_name = "file"
    queryset = FileRepository.objects.all()
    serializer_class = FileRepositorySerializer

    @extend_schema(
        description="Trigger an asynchronous task to sync file content.",
        responses={202: AsyncOperationResponseSerializer},
    )
    @action(detail=True, methods=["post"], serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Synchronizes a repository.

        The ``repository`` field has to be provided.
        """
        serializer = RepositorySyncURLSerializer(
            data=request.data, context={"request": request, "repository_pk": pk}
        )
        serializer.is_valid(raise_exception=True)

        repository = self.get_object()
        remote = serializer.validated_data.get("remote", repository.remote)

        mirror = serializer.validated_data.get("mirror", False)
        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={"remote_pk": remote.pk, "repository_pk": repository.pk, "mirror": mirror},
        )
        return OperationPostponedResponse(result, request)


class FileRepositoryVersionViewSet(RepositoryVersionViewSet):
    """
    <!-- User-facing documentation, rendered as html-->
    FileRepositoryVersion represents a single file repository version.
    """

    parent_viewset = FileRepositoryViewSet


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


class FilePublicationViewSet(PublicationViewSet):
    """
    <!-- User-facing documentation, rendered as html-->
    A FilePublication contains metadata about all the <a
    href="#operation/content_file_files_list">File Content</a> in a particular <a
    href="href="#tag/repositories:-file-versions">File Repository Version.</a>
    Once a FilePublication has been created, it can be hosted using the
    <a href="#operation/distributions_file_file_list">File Distribution API.</a>
    """

    endpoint_name = "file"
    queryset = FilePublication.objects.exclude(complete=False)
    serializer_class = FilePublicationSerializer

    @extend_schema(
        description="Trigger an asynchronous task to publish file content.",
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


class FileFilesystemExporterViewSet(ExporterViewSet):
    """
    FilesystemExporters export content from a publication to a path on the file system.

    WARNING: This feature is provided as a tech preview and may change in the future. Backwards
    compatibility is not guaranteed.
    """

    endpoint_name = "filesystem"
    queryset = FileFilesystemExporter.objects.all()
    serializer_class = FileFilesystemExporterSerializer


class FileFilesystemExportViewSet(ExportViewSet):
    """
    FilesystemExports provide a history of previous exports.
    """

    parent_viewset = FileFilesystemExporterViewSet

    @extend_schema(
        request=PublicationExportSerializer,
        description="Trigger an asynchronous task to export a file publication.",
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request, exporter_pk):
        """
        Export a publication to the file system.

        The ``repository`` field has to be provided.
        """
        try:
            exporter = FileFilesystemExporter.objects.get(pk=exporter_pk)
        except FileFilesystemExporter.DoesNotExist:
            raise Http404

        serializer = PublicationExportSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        publication = serializer.validated_data.get("publication")
        result = enqueue_with_reservation(
            fs_publication_export,
            [publication, exporter],
            kwargs={"exporter_pk": exporter.pk, "publication_pk": publication.pk},
        )
        return OperationPostponedResponse(result, request)
