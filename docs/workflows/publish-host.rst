Publish and Host
================

This section assumes that you have a repository with content in it (a repository version). To do
this, see the :doc:`sync` or :doc:`upload` documentation.

Create a Publication (manually)
-------------------------------

.. literalinclude:: ../_scripts/publication.sh
   :language: bash

Publication GET Response (after task is complete)::

    {
        "pulp_created": "2019-05-16T19:28:42.971611Z",
        "pulp_href": "/pulp/api/v3/publications/file/file/7d5440f6-202c-4e71-ace2-14c534f6df9e/",
        "distributions": [],
        "publisher": null,
        "repository": "/pulp/api/v3/repositories/e242c556-bf46-4330-9c81-0be5432e55ba/file/file/",
        "repository_version": "/pulp/api/v3/repositories/e242c556-bf46-4330-9c81-0be5432e55ba/file/file/versions/1/"
    }

Reference: `File Publication Usage <../restapi.html#tag/publications>`_

Create a Distribution for the Publication
-----------------------------------------

.. literalinclude:: ../_scripts/distribution.sh
   :language: bash

Distribution GET Response (after task is complete)::

    {
        "pulp_created": "2019-05-16T19:28:45.135868Z",
        "pulp_href": "/pulp/api/v3/distributions/file/file/9e9e07cb-b30f-41c5-a98b-583185f907e2/",
        "base_path": "foo",
        "base_url": "localhost:24816/pulp/content/foo",
        "content_guard": null,
        "name": "baz",
        "repository": null,
        "publication": "/pulp/api/v3/publications/file/file/7d5440f6-202c-4e71-ace2-14c534f6df9e/"
    }

Reference: `File Distribution Usage <../restapi.html#tag/distributions>`_

Download ``1.iso`` from Pulp
---------------------------------

If you created your repository version using the :doc:`sync` workflow:

.. literalinclude:: ../_scripts/download_after_sync.sh
   :language: bash

If you created your repository version using the :doc:`upload` workflow:

.. literalinclude:: ../_scripts/download_after_upload.sh
   :language: bash

Automate Publication and Distribution
-------------------------------------

With a little more initial setup, you can have publications and distributions for your repositories
updated automatically when new repository versions are created.

.. code-block:: bash

    # This configures the repository to produce new publications when a new version is created
    pulp file repository update --name $REPO_NAME --autopublish

    # This configures the distribution to be track the latest repository version for a given repository
    pulp file distribution update --name $DIST_NAME --repository $REPO_NAME

.. warning::
    Support for automatic publication and distribution is provided as a tech preview in Pulp 3.
    Functionality may not work or may be incomplete. Also, backwards compatibility when upgrading
    is not guaranteed.
