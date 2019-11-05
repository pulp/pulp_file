import logging

from gettext import gettext as _

from pulp_file.app.models import FileFileSystemExporter, FilePublication


log = logging.getLogger(__name__)


def file_export(exporter_pk, publication_pk):
    """
    Export a Publication to the file system.

    Args:
        exporter_pk (str): FileFileSystemExporter pk
        publication_pk (str): FilePublication pk

    """
    exporter = FileFileSystemExporter.objects.get(pk=exporter_pk)
    publication = FilePublication.objects.get(pk=publication_pk)

    log.info(
        _(
            "Exporting: file_system_exporter={exporter}, publication={publication}, path=path"
        ).format(exporter=exporter.name, publication=publication.pk, path=exporter.path)
    )

    exporter.export(publication)

    log.info(_("Publication: {publication} exported").format(publication=publication.pk))
