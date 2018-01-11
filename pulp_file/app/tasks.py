from collections import namedtuple
from contextlib import suppress
from gettext import gettext as _
from urllib.parse import urlparse, urlunparse
import logging
import os

from celery import shared_task
from django.db import transaction
from django.db.models import Q
from pulpcore.plugin import models
from pulpcore.plugin.tasks import working_dir_context, UserFacingTask

from pulpcore.plugin.changeset import (
    BatchIterator,
    ChangeSet,
    PendingArtifact,
    PendingContent,
    SizedIterable,
)

from pulp_file.app import models as file_models
from pulp_file.manifest import Manifest

log = logging.getLogger(__name__)


# Natural key.
Key = namedtuple('Key', ('path', 'digest'))


@shared_task(base=UserFacingTask)
def sync(importer_pk):
    """
    Call sync on the importer defined by a plugin.

    Check that the importer has a feed_url, which is necessary to sync. A working directory
    is prepared, the plugin's sync is called, and then working directory is removed.

    Args:
        importer_pk (str): The importer PK.

    Raises:
        ValueError: When feed_url is empty.
    """
    importer = file_models.FileImporter.objects.get(pk=importer_pk)

    if not importer.feed_url:
        raise ValueError(_("An importer must have a 'feed_url' attribute to sync."))

    with transaction.atomic():
        new_version = models.RepositoryVersion(repository=importer.repository)
        new_version.save()
        created = models.CreatedResource(content_object=new_version)
        created.save()

    base_version = None
    with suppress(models.RepositoryVersion.DoesNotExist):
        base_version = importer.repository.versions.latest()

    with working_dir_context():
        log.info(
            _('Starting sync: repository=%(repository)s importer=%(importer)s'),
            {
                'repository': importer.repository.name,
                'importer': importer.name
            })
        try:
            Synchronizer(importer, new_version, base_version).run()
        except Exception:
            new_version.delete()
            raise


class Synchronizer:
    """
    Repository synchronizer for FileContent

    This object walks through the full standard workflow of running a sync. See the "run" method
    for details on that workflow.
    """

    def __init__(self, importer, new_version, old_version):
        """
        Args:
            importer (Importer): the importer to use for the sync operation
            new_version (pulpcore.plugin.models.RepositoryVersion): the new version to which content
                should be added and removed.
            old_version (pulpcore.plugin.models.RepositoryVersion): the latest pre-existing version
                or None if one does not exist.
        """
        self._importer = importer
        self._new_version = new_version
        self._old_version = old_version
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
        parsed_url = urlparse(self._importer.feed_url)
        download = self._importer.get_futures_downloader(
            self._importer.feed_url, os.path.basename(parsed_url.path))
        download()
        self._manifest = Manifest(download.writer.path)

    def _fetch_inventory(self):
        """
        Fetch existing content in the repository.
        """
        # it's not a problem if there is no pre-existing version.
        if self._old_version is not None:
            q_set = self._old_version.content()
            for content in (c.cast() for c in q_set):
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
            file = file_models.FileContent(path=entry.path, digest=entry.digest)
            artifact = models.Artifact(size=entry.size, sha256=entry.digest)

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
            q_set = self._old_version.content().filter(q)
            q_set = q_set.only('id')
            for content in q_set:
                yield content
