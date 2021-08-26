from django_filters import CharFilter
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from pulpcore.plugin.actions import ModifyRepositoryActionMixin
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import dispatch
from pulpcore.plugin.viewsets import (
    AlternateContentSourceViewSet,
    ContentFilter,
    DistributionViewSet,
    OperationPostponedResponse,
    PublicationViewSet,
    RemoteViewSet,
    RepositoryViewSet,
    RepositoryVersionViewSet,
    SingleArtifactContentUploadViewSet,
)

from . import tasks
from .models import (
    FileAlternateContentSource,
    FileContent,
    FileDistribution,
    FileRemote,
    FileRepository,
    FilePublication,
)
from .serializers import (
    FileAlternateContentSourceSerializer,
    FileContentSerializer,
    FileDistributionSerializer,
    FileRemoteSerializer,
    FileRepositorySerializer,
    FilePublicationSerializer,
)


class FileContentFilter(ContentFilter):
    """
    FilterSet for FileContent.
    """

    sha256 = CharFilter(field_name="digest")

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
        result = dispatch(
            tasks.synchronize,
            [repository, remote],
            kwargs={
                "remote_pk": str(remote.pk),
                "repository_pk": str(repository.pk),
                "mirror": mirror,
            },
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

        result = dispatch(
            tasks.publish,
            [repository_version.repository],
            kwargs={"repository_version_pk": str(repository_version.pk), "manifest": str(manifest)},
        )
        return OperationPostponedResponse(result, request)


class FileDistributionViewSet(DistributionViewSet):
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


class FileAlternateContentSourceViewSet(AlternateContentSourceViewSet):
    """
    Alternate Content Source ViewSet for File

    ACS support is provided as a tech preview in pulp_file.
    """

    endpoint_name = "file"
    queryset = FileAlternateContentSource.objects.all()
    serializer_class = FileAlternateContentSourceSerializer
