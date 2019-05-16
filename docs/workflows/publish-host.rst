Publish and Host
================

This section assumes that you have a repository with content in it (a repository version). To do
this, see the :doc:`sync` or :doc:`upload` documentation.

Create a Publication
--------------------

``$ http POST http://localhost:24817/pulp/api/v3/publications/file/file/ repository=$REPO_HREF``

.. code:: json

    {
        "task": "/pulp/api/v3/tasks/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/"
    }

``$ export PUBLICATION_HREF=$(http :24817/pulp/api/v3/publications/file/file/ | jq -r '.results[0] | ._href')``

Reference: `File Publication Usage <../restapi.html#tag/publications>`_

Create a Distribution for the Publication
-----------------------------------------

``$ http POST http://localhost:24817/pulp/api/v3/distributions/file/file/ name='baz' base_path='foo' publication=$PUBLICATION_HREF``

Reference: `File Distribution Usage <../restapi.html#tag/distributions>`_

Download ``foo.tar.gz`` from Pulp
---------------------------------

``$ http GET http://localhost:24816/pulp/content/foo/foo.tar.gz``
