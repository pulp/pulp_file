import hashlib
import os

from collections import namedtuple
from gettext import gettext as _
from logging import getLogger
from urllib.parse import urlparse, urlunparse

from django.core.files import File
from django.db import models
from django.db.utils import IntegrityError

from pulpcore.download import DigestValidation, DownloadError, SizeValidation
from pulpcore.plugin.tasking import Task as current_task
from pulpcore.plugin.models import (Artifact, Content, ContentArtifact, DeferredArtifact, Importer,
    ProgressBar, Publisher, RepositoryContent)
from pulpcore.plugin.changeset import (
    BatchIterator, ChangeSet, SizedIterable, RemoteContent, RemoteArtifact,
    ChangeReport, ChangeFailed)

from pulp_file.manifest import Manifest


log = getLogger(__name__)

BUFFER_SIZE = 65536

# Changes needed.
Delta = namedtuple('Delta', ('additions', 'removals'))
# Natural key.
FileTuple = namedtuple('Key', ('path', 'digest', 'size'))


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


class PulpManifestMixin(object):
    """
    Provides functions for working with an importer's PULP_MANIFEST.
    """
    def _fetch_inventory(self):
        """
        Fetch existing content in the repository.

        Returns:
            set: of Key.
        """
        inventory = set()
        q_set = FileContent.objects.filter(repositories=self.repository)
        q_set = q_set.only(*[f.name for f in FileContent.natural_key_fields])
        for content in (c.cast() for c in q_set):
            key = FileTuple(path=content.path, digest=content.digest,size=content.size)
            inventory.add(key)
        return inventory

    def _fetch_manifest(self):
        """
        Fetch (download) the manifest.

        Returns:
            Manifest: The manifest.
        """
        parsed_url = urlparse(self.feed_url)
        download = self.get_download(self.feed_url, os.path.basename(parsed_url.path))
        download()
        return Manifest(download.writer.path)

    @staticmethod
    def _find_delta(manifest, inventory, mirror=True):
        """
        Using the manifest and set of existing (natural) keys,
        determine the set of content to be added and deleted from the
        repository.  Expressed in natural key.
        Args:
            manifest (Manifest): The fetched manifest.
            inventory (set): Set of existing content (natural) keys.
            mirror (bool): Faked mirror option.
                TODO: should be replaced with something standard.

        Returns:
            Delta: The needed changes.
        """
        remote = set()
        for entry in manifest.read():
            key = FileTuple(path=entry.path, digest=entry.digest, size=entry.size)
            remote.add(key)
        additions = remote - inventory
        if mirror:
            removals = inventory - remote
        else:
            removals = set()
        return Delta(additions=additions, removals=removals)



class FileImporter(Importer, PulpManifestMixin):
    """
    Importer for "file" content that uses ChangeSets to perform the sync.

    This importer uses the ChangeSet API to download content in parallel and import into the
    repository. Any content removed from the remote repository since the previous sync is also
    removed from the Pulp repository.
    """
    TYPE = 'file'

    def sync(self):
        """
        Synchronize the repository with the remote repository.
        """
        failed = 0
        added = 0
        removed = 0

        # TODO: Change logging WARN to INFO.
        # logging at WARN until logging is properly configured.

        log.warn(
            _('FileImporter: synchronizing repository %(r)s'),
            {
                'r': self.repository.name
            })

        changeset = self._build_changeset()
        for report in changeset.apply():
            try:
                report.result()
            except ChangeFailed:
                failed += 1
            else:
                if report.action == ChangeReport.ADDED:
                    added += 1
                else:
                    removed += 1

        log.warn(
            _('FileImporter: total: added:%(a)d, removed:%(r)d, failed %(f)d'),
            {
                'a': added,
                'r': removed,
                'f': failed
            })
        # On failed > 0, raise a PulpCodedException?
        # Done

    def _build_additions(self, manifest, delta):
        """
        Generate the content to be added.

        Args:
            manifest (Manifest): The fetched manifest.
            delta (Delta): The needed changes.

        Returns:
            generator: A generator of content to be added.
        """
        parsed_url = urlparse(self.feed_url)
        root_dir = os.path.dirname(parsed_url.path)
        for entry in manifest.read():
            key = FileTuple(path=entry.path, digest=entry.digest, size=entry.size)
            if key not in delta.additions:
                continue
            path = os.path.join(root_dir, entry.path)
            url = urlunparse(parsed_url._replace(path=path))
            content = FileContent(path=entry.path, digest=entry.digest)
            remote_content = RemoteContent(content)
            artifact = Artifact(relative_path=entry.path, sha256=entry.digest)
            download = self.get_download(url, entry.path, artifact)
            remote_artifact = RemoteArtifact(artifact, download)
            remote_content.artifacts.add(remote_artifact)
            yield remote_content

    def _fetch_removals(self, delta):
        """
        Generate the content to be removed.

        Args:
            delta (Delta): The needed changes.

        Returns:
            generator: A generator of content to be removed.

        """
        for natural_keys in BatchIterator(delta.removals):
            q = models.Q()
            for key in natural_keys:
                q |= models.Q(filecontent__path=key.path, filecontent__digest=key.digest)
            q_set = self.repository.content.filter(q)
            q_set = q_set.only('artifacts')
            for content in q_set:
                yield content

    def _is_deferred(self):
        """
        Get whether downloading is deferred.

        Returns:
            bool: True when deferred.
        """
        return self.download_policy != 'immediate'

    def _build_changeset(self):
        """
        Build a change set.

        Returns:
            ChangeSet: The built `ChangeSet`.

        """
        inventory = self._fetch_inventory()
        manifest = self._fetch_manifest()
        delta = self._find_delta(manifest, inventory)
        additions = SizedIterable(
            self._build_additions(manifest, delta),
            len(delta.additions))
        removals = SizedIterable(
            self._fetch_removals(delta),
            len(delta.removals))
        changeset = ChangeSet(self, additions=additions, removals=removals)
        changeset.deferred = self._is_deferred()
        return changeset


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


class BasicFileImporter(Importer, PulpManifestMixin):
    """
    Importer for "file" content.

    This importer uses the plugin API to download content serially and import it into the
    repository. Any content removed from the remote repository since the previous sync is also
    removed from the Pulp repository.
    """
    TYPE = 'file'

    def sync(self):
        """
        Synchronize the repository with the remote repository.
        """
        inventory = self._fetch_inventory()
        manifest = self._fetch_manifest()
        delta = self._find_delta(manifest, inventory)
        parsed_url = urlparse(self.feed_url)
        root_dir = os.path.dirname(parsed_url.path)

        # Start reporting progress
        if self.download_policy != self.IMMEDIATE:
            description = _("Adding file content to the repository without downloading artifacts.")
        else:
            description = _("Dowloading artifacts and adding content to the repository.")
        progress_bar = ProgressBar(message=description, total=len(delta.additions))
        progress_bar.save()

        # Add content and report progress while doing so
        with progress_bar:
            for entry in delta.additions:
                path = os.path.join(root_dir, entry.path)
                url = urlunparse(parsed_url._replace(path=path))
                content, content_created = FileContent.objects.get_or_create(path=entry.path,
                                                                             digest=entry.digest)
                # Add content to the repository
                association = RepositoryContent(
                    repository=self.repository,
                    content=content)
                association.save()
                # ContentArtifact is required for all download policies. It is used for publishing.
                content_artifact, content_artifact_created = ContentArtifact.objects.get_or_create(
                    content=content, relative_path=entry.path)
                # DeferredArtifact is required for deferred download policies.
                deferred_artifact, deferred_artifact_created = \
                    DeferredArtifact.objects.get_or_create(
                    url=url, importer=self, content_artifact=content_artifact, sha256=entry.digest)

                if self.download_policy != self.IMMEDIATE:
                    # Set Artifact ID if the Artifact already exists and then continue
                    try:
                        artifact = Artifact.objects.get(sha256=entry.digest)
                        content_artifact.artifact = artifact
                    except Artifact.DoesNotExist:
                        pass
                    content_artifact.save()
                    # Report progress
                    progress_bar.increment()
                    continue

                try:
                    artifact = Artifact.objects.get(sha256=entry.digest)
                except Artifact.DoesNotExist:
                    download = self.get_download(url, entry.path)
                    download.validations.append(SizeValidation(entry.size))
                    download.validations.append(DigestValidation('sha256', entry.digest))
                    try:
                        download()
                    except DownloadError as e:
                        # Remove content and it's association with repository. Don't report
                        # progress.
                        association.delete()
                        if content_created:
                            content.delete()
                        if deferred_artifact_created:
                            deferred_artifact.delete()
                        # record non-fatal exception
                        current_task.append_non_fatal_error(e)
                        continue
                    else:
                        with File(open(download.writer.path, mode='rb')) as file:
                            checksums = self.get_checksums(file)
                            try:
                                artifact = Artifact(file=file, size=file.size, **checksums)
                                artifact.save()
                            except IntegrityError:
                                artifact = Artifact.objects.get(sha256=checksums['sha256'])
                            except:
                                association.delete()
                                if content_created:
                                    content.delete()
                                if deferred_artifact_created:
                                    deferred_artifact.delete()
                content_artifact.artifact = artifact
                # Save ContentArtifact now that it has artifact set.
                content_artifact.save()
                # Report progress
                progress_bar.increment()

        # Remove content if there is any to remove
        if delta.removals:
            # Build a query that uniquely identifies all content that needs to be removed.
            q = models.Q()
            for key in delta.removals:
                q |= models.Q(filecontent__path=key.path, filecontent__digest=key.digest)
            q_set = self.repository.content.filter(q)
            RepositoryContent.objects.filter(
                repository=self.repository).filter(content=q_set).delete()

    @staticmethod
    def get_checksums(file):
        """
        Calculates all checksums for a file.

        Args:
            file (:class:`django.core.files.File`): open file handle

        Returns:
            dict: Dictionary where keys are checksum names and values are checksum values
        """
        hashers = {}
        for algorithm in hashlib.algorithms_guaranteed:
            hashers[algorithm] = getattr(hashlib, algorithm)()
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            for algorithm, hasher in hashers.items():
                hasher.update(data)
        ret = {}
        for algorithm, hasher in hashers.items():
            ret[algorithm] = hasher.hexdigest()
        return ret
