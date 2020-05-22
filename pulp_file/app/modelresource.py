from pulpcore.plugin.importexport import BaseContentResource
from pulp_file.app.models import FileContent


class FileContentResource(BaseContentResource):
    """
    Resource for import/export of file_filecontent entities
    """

    def set_up_queryset(self):
        """
        :return: FileContents specific to a specified repo-version.
        """
        return FileContent.objects.filter(pk__in=self.repo_version.content)

    class Meta:
        model = FileContent
        import_id_fields = model.natural_key_fields()


IMPORT_ORDER = [FileContentResource]
