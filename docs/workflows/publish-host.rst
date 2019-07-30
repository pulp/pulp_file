Publish and Host
================

This section assumes that you have a repository with content in it (a repository version). To do
this, see the :doc:`sync` or :doc:`upload` documentation.

Create a Publication
--------------------

.. literalinclude:: ../_scripts/publication.sh
   :language: bash

Publication GET Response (after task is complete)::

    {
        "_created": "2019-05-16T19:28:42.971611Z",
        "_href": "/pulp/api/v3/publications/file/file/7d5440f6-202c-4e71-ace2-14c534f6df9e/",
        "_type": "file.file",
        "distributions": [],
        "publisher": null,
        "repository": "http://localhost:24817/pulp/api/v3/repositories/%3CRepository:%20foo%3E/",
        "repository_version": "/pulp/api/v3/repositories/e242c556-bf46-4330-9c81-0be5432e55ba/versions/1/"
    }

Reference: `File Publication Usage <../restapi.html#tag/publications>`_

Create a Distribution for the Publication
-----------------------------------------

.. literalinclude:: ../_scripts/distribution.sh
   :language: bash

Distribution GET Response (after task is complete)::

    {
        "_created": "2019-05-16T19:28:45.135868Z",
        "_href": "/pulp/api/v3/distributions/file/file/9e9e07cb-b30f-41c5-a98b-583185f907e2/",
        "base_path": "foo",
        "base_url": "localhost:24816/pulp/content/foo",
        "content_guard": null,
        "name": "baz",
        "publication": "/pulp/api/v3/publications/file/file/7d5440f6-202c-4e71-ace2-14c534f6df9e/"
    }

Reference: `File Distribution Usage <../restapi.html#tag/distributions>`_

Download ``test.iso`` from Pulp
---------------------------------

If you created your repository version using the :doc:`sync` workflow:

.. literalinclude:: ../_scripts/download_after_sync.sh
   :language: bash

If you created your repository version using the :doc:`upload` workflow:

.. literalinclude:: ../_scripts/download_after_upload.sh
   :language: bash
