import os

from collections import namedtuple
from logging import getLogger
from urllib.parse import urlparse, urlunparse

from django.db import models

from pulpcore.plugin.models import Artifact, Content, Importer, Publisher
from pulpcore.plugin.changeset import (
    BatchIterator,
    ChangeSet,
    PendingArtifact,
    PendingContent,
    SizedIterable,
)

from pulp_file.manifest import Manifest


log = getLogger(__name__)


# Natural key.
Key = namedtuple('Key', ('path', 'digest'))


class FileContent(Content):
    """
    The "file" content type.

    Content of this type represents a collection of 0 or more files uniquely
    identified by path and SHA256 digest.

    Fields:
        path (str): The file relative path.
        digest (str): The SHA256 HEX digest.

    """
    TYPE = 'file'

    path = models.TextField(blank=False, null=False)
    digest = models.TextField(blank=False, null=False)

    natural_key_fields = (path, digest)

    class Meta:
        unique_together = (
            'path',
            'digest'
        )

    def natural_key(self):
        """
        Get the model's natural key.

        Returns:
            Key: The natural key.
        """
        return Key(path=self.path, digest=self.digest)


class FileImporter(Importer):
    """
    Importer for "file" content.
    """
    TYPE = 'file'

    def sync(self):
        """
        Synchronizes the repository by calling the FileSync class.
        """
        Synchronizer(self).run()


class Synchronizer:
    """
    Repository synchronizer for FileContent

    This object walks through the full standard workflow of running a sync. See the "run" method
    for details on that workflow.
    """

    def __init__(self, importer):
        """
        Args:
            importer (Importer): the importer to use for the sync operation
        """
        self._importer = importer
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
        changeset = ChangeSet(self._importer, additions=additions, removals=removals)
        changeset.apply_and_drain()

    def _fetch_manifest(self):
        """
        Fetch (download) the manifest.
        """
        parsed_url = urlparse(self._importer.feed_url)
        download = self._importer.get_download(
            self._importer.feed_url, os.path.basename(parsed_url.path))
        download()
        self._manifest = Manifest(download.writer.path)

    def _fetch_inventory(self):
        """
        Fetch existing content in the repository.
        """
        q_set = FileContent.objects.filter(repositories=self._importer.repository)
        q_set = q_set.only(*[f.name for f in FileContent.natural_key_fields])
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
            q = models.Q()
            for key in natural_keys:
                q |= models.Q(filecontent__path=key.path, filecontent__digest=key.digest)
            q_set = self._importer.repository.content.filter(q)
            q_set = q_set.only('artifacts')
            for content in q_set:
                yield content


class FilePublisher(Publisher):
    """
    Publisher for "file" content.
    """
    TYPE = 'file'

    def publish(self):
        """
        Perform a publish.

        Publish behavior for the file plugin has not yet been implemented.
        """
        raise NotImplementedError
