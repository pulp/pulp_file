import logging
import os

from collections import namedtuple
from gettext import gettext as _
from urllib.parse import urlparse, urlunparse

from celery import shared_task
from django.core.files import File
from django.db.models import Q

from pulpcore.plugin.models import (
    Artifact,
    RepositoryVersion,
    Publication,
    PublishedArtifact,
    PublishedMetadata,
    RemoteArtifact,
    Repository)
from pulpcore.plugin.changeset import (
    BatchIterator,
    ChangeSet,
    PendingArtifact,
    PendingContent,
    SizedIterable)
from pulpcore.plugin.tasking import UserFacingTask, WorkingDirectory

from pulp_file.app.models import FileContent, FileImporter, FilePublisher
from pulp_file.manifest import Entry, Manifest


log = logging.getLogger(__name__)


# Natural key.
Key = namedtuple('Key', ('path', 'digest'))


def _publish(publication):
    """
    Create published artifacts and yield a Manifest Entry for each.

    Args:
        publication (pulpcore.plugin.models.Publication): The Publication being created.

    Yields:
        Entry: The manifest entry.
    """
    def find_artifact():
        _artifact = content_artifact.artifact
        if not _artifact:
            _artifact = RemoteArtifact.objects.filter(content_artifact=content_artifact).first()
        return _artifact
    paths = set()
    for content in FileContent.objects.filter(
            pk__in=publication.repository_version.content).order_by('-created'):
        if content.path in paths:
            continue
        paths.add(content.path)
        for content_artifact in content.contentartifact_set.all():
            artifact = find_artifact()
            published_artifact = PublishedArtifact(
                relative_path=content_artifact.relative_path,
                publication=publication,
                content_artifact=content_artifact)
            published_artifact.save()
            entry = Entry(
                path=content_artifact.relative_path,
                digest=artifact.sha256,
                size=artifact.size)
            yield entry


@shared_task(base=UserFacingTask)
def publish(publisher_pk, repository_pk):
    """
    Use provided publisher to create a Publication based on a RepositoryVersion.

    Args:
        publisher_pk (str): Use the publish settings provided by this publisher.
        repository_pk (str): Create a Publication from the latest version of this Repository.
    """
    publisher = FilePublisher.objects.get(pk=publisher_pk)
    repository = Repository.objects.get(pk=repository_pk)
    repository_version = RepositoryVersion.latest(repository)

    log.info(
        _('Publishing: repository=%(repository)s, version=%(version)d, publisher=%(publisher)s'),
        {
            'repository': repository.name,
            'version': repository_version.number,
            'publisher': publisher.name,
        })

    with WorkingDirectory():
        with Publication.create(repository_version, publisher) as publication:
            manifest = Manifest('PULP_MANIFEST')
            manifest.write(_publish(publication))
            metadata = PublishedMetadata(
                relative_path=os.path.basename(manifest.path),
                publication=publication,
                file=File(open(manifest.path, 'rb')))
            metadata.save()

    log.info(
        _('Publication: %(publication)s created'),
        {
            'publication': publication.pk
        })


@shared_task(base=UserFacingTask)
def sync(importer_pk, repository_pk):
    """
    Validate the importer, create and finalize RepositoryVersion.

    Args:
        importer_pk (str): The importer PK.

    Raises:
        ValueError: When feed_url is empty.
    """
    importer = FileImporter.objects.get(pk=importer_pk)
    repository = Repository.objects.get(pk=repository_pk)

    if not importer.feed_url:
        raise ValueError(_("An importer must have a 'feed_url' attribute to sync."))

    base_version = RepositoryVersion.latest(repository)

    with RepositoryVersion.create(repository) as new_version:

        synchronizer = Synchronizer(importer, new_version, base_version)
        with WorkingDirectory():
            log.info(
                _('Starting sync: repository=%(repository)s importer=%(importer)s'),
                {
                    'repository': repository.name,
                    'importer': importer.name
                })
            synchronizer.run()


class Synchronizer:
    """
    Repository synchronizer for FileContent

    This object walks through the full standard workflow of running a sync. See the "run" method
    for details on that workflow.
    """

    def __init__(self, importer, new_version, base_version):
        """
        Args:
            importer (Importer): the importer to use for the sync operation
            new_version (pulpcore.plugin.models.RepositoryVersion): the new version to which content
                should be added and removed.
            base_version (pulpcore.plugin.models.RepositoryVersion): the latest version
                or None if one does not exist.
        """
        self._importer = importer
        self._new_version = new_version
        self._base_version = base_version
        self._manifest = None
        self._inventory_keys = set()
        self._keys_to_add = set()
        self._keys_to_remove = set()

    def run(self):
        """
        Synchronize the repository with the remote repository.

        This walks through the standard workflow that most sync operations want to follow. This
        pattern is a recommended starting point for other plugins.

        - Determine what is available remotely.
        - Determine what is already in the local repository.
        - Compare those two, and based on any importer settings or content-type-specific logic,
          figure out what you want to add and remove from the local repository.
        - Use a ChangeSet to make those changes happen.
        """
        # Determine what is available remotely
        self._fetch_manifest()
        # Determine what is already in the repo
        self._fetch_inventory()

        # Based on the above two, figure out what we want to add and remove
        self._find_delta()
        additions = SizedIterable(
            self._build_additions(),
            len(self._keys_to_add))
        removals = SizedIterable(
            self._build_removals(),
            len(self._keys_to_remove))

        # Hand that to a ChangeSet, and we're done!
        changeset = ChangeSet(self._importer, self._new_version, additions=additions,
                              removals=removals)
        changeset.apply_and_drain()

    def _fetch_manifest(self):
        """
        Fetch (download) the manifest.
        """
        downloader = self._importer.get_downloader(self._importer.feed_url)
        downloader.fetch()
        self._manifest = Manifest(downloader.path)

    def _fetch_inventory(self):
        """
        Fetch existing content in the repository.
        """
        # it's not a problem if there is no pre-existing version.
        if self._base_version is not None:
            for content in FileContent.objects.filter(pk__in=self._base_version.content):
                key = Key(path=content.path, digest=content.digest)
                self._inventory_keys.add(key)

    def _find_delta(self, mirror=True):
        """
        Using the manifest and set of existing (natural) keys,
        determine the set of content to be added and deleted from the
        repository.  Expressed in natural key.

        Args:
            mirror (bool): Faked mirror option.
                TODO: should be replaced with something standard.

        """
        # These keys are available remotely. Storing just the natural key makes it memory-efficient
        # and thus reasonable to hold in RAM even with a large number of content units.
        remote_keys = set([Key(path=e.path, digest=e.digest) for e in self._manifest.read()])

        self._keys_to_add = remote_keys - self._inventory_keys
        if mirror:
            self._keys_to_remove = self._inventory_keys - remote_keys

    def _build_additions(self):
        """
        Generate the content to be added.

        This makes a second pass through the manifest. While it does not matter a lot for this
        plugin specifically, many plugins cannot hold the entire index of remote content in memory
        at once. They must reduce that to only the natural keys, decide which to retrieve
        (self.keys_to_add in our case), and then re-iterate the index to access each full entry one
        at a time.

        Returns:
            generator: A generator of content to be added.
        """
        parsed_url = urlparse(self._importer.feed_url)
        root_dir = os.path.dirname(parsed_url.path)

        for entry in self._manifest.read():
            # Determine if this is an entry we decided to add.
            key = Key(path=entry.path, digest=entry.digest)
            if key not in self._keys_to_add:
                continue

            # Instantiate the content and artifact based on the manifest entry.
            path = os.path.join(root_dir, entry.path)
            url = urlunparse(parsed_url._replace(path=path))
            file = FileContent(path=entry.path, digest=entry.digest)
            artifact = Artifact(size=entry.size, sha256=entry.digest)

            # Now that we know what we want to add, hand it to "core" with the API objects.
            content = PendingContent(
                file,
                artifacts={
                    PendingArtifact(artifact, url, entry.path)
                })
            yield content

    def _build_removals(self):
        """
        Generate the content to be removed.

        Returns:
            generator: A generator of FileContent instances to remove from the repository
        """
        for natural_keys in BatchIterator(self._keys_to_remove):
            q = Q()
            for key in natural_keys:
                q |= Q(filecontent__path=key.path, filecontent__digest=key.digest)
            q_set = self._base_version.content.filter(q)
            q_set = q_set.only('id')
            for content in q_set:
                yield content
