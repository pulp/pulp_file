Export
======

Filesystem
----------

This section describes how to export file content to the filesystem. Exporting content to the
filesystem is useful if you want to serve content with your own web server and not use Pulp's
Content App, or if you want to transfer your content to another location (via rsync, etc).

If DEFAULT_FILE_STORAGE is filesystem, the FilesystemExporter will create hard links. Otherwise, it
will fetch and write the content to the filesystem.

This example assumes you have a Publication and that publication's href is stored as
$PUBLICATION_HREF. 

First, create a FilesystemExporter and give it the desired path. Your ALLOWED_EXPORT_PATHS setting must
include this path.

.. literalinclude:: ../_scripts/exporter.sh
   :language: bash

Next you can use this exporter to create a filesystem export that will export your Publication's
content to the filesystem.

.. literalinclude:: ../_scripts/export.sh
   :language: bash
