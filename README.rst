``pulp_file`` Plugin
====================

This is the ``pulp_file`` Plugin for `Pulp Project
3.0+ <https://pypi.org/project/pulpcore/>`__. This plugin replaces the ISO support in the
``pulp_rpm`` plugin for Pulp 2. This plugin uses the
`ChangeSet API <http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-api/changeset.html>`_
to add and remove content from a repository.

All REST API examples bellow use `httpie <https://httpie.org/doc>`__ to perform the requests.
The ``httpie`` commands below assume that the user executing the commands has a ``.netrc`` file
in the home directory. The ``.netrc`` should have the following configuration:

.. code-block::

    machine localhost
    login admin
    password admin

If you configured the ``admin`` user with a different password, adjust the configuration
accordingly. If you prefer to specify the username and password with each request, please see
``httpie`` documentation on how to do that.

This documentation makes use of the `jq library <https://stedolan.github.io/jq/>`_
to parse the json received from requests, in order to get the unique urls generated
when objects are created. To follow this documentation as-is please install the jq
library with:

``$ sudo dnf install jq``

Install ``pulpcore``
--------------------

Follow the `installation
instructions <https://docs.pulpproject.org/en/3.0/nightly/installation/instructions.html>`__
provided with pulpcore.

Users should install from **either** PyPI or source.

Install ``pulp-file`` from source
---------------------------------

.. code-block:: bash

   sudo -u pulp -i
   source ~/pulpvenv/bin/activate
   git clone https://github.com/pulp/pulp_file.git
   cd pulp_file
   pip install -e .

Install ``pulp-file`` From PyPI
-------------------------------

.. code-block:: bash

   sudo -u pulp -i
   source ~/pulpvenv/bin/activate
   pip install pulp-file

Make and Run Migrations
-----------------------

.. code-block:: bash

   export DJANGO_SETTINGS_MODULE=pulpcore.app.settings
   django-admin makemigrations file
   django-admin migrate file

Run Services
------------

.. code-block:: bash

   django-admin runserver 24817
   gunicorn pulpcore.content:server --bind 'localhost:24816' --worker-class 'aiohttp.GunicornWebWorker' -w 2
   sudo systemctl restart pulp-resource-manager
   sudo systemctl restart pulp-worker@1
   sudo systemctl restart pulp-worker@2


Create a repository ``foo``
---------------------------

``$ http POST http://localhost:24817/pulp/api/v3/repositories/ name=foo``

.. code:: json

    {
        "_href": "/pulp/api/v3/repositories/696c8cf3-3ad6-4af9-a007-e6c43272df94/",
        ...
    }

``$ export REPO_HREF=$(http :24817/pulp/api/v3/repositories/ | jq -r '.results[] | select(.name == "foo") | ._href')``

Create a new remote ``bar``
---------------------------

``$ http POST http://localhost:24817/pulp/api/v3/remotes/file/file/ name='bar' url='https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST'``

.. code:: json

    {
        "_href": "/pulp/api/v3/remotes/file/file/8098cf53-df95-4889-bb3b-3c10e23063ce/",
        ...
    }

``$ export REMOTE_HREF=$(http :24817/pulp/api/v3/remotes/file/file/ | jq -r '.results[] | select(.name == "bar") | ._href')``

Sync repository ``foo`` using remote ``bar``
--------------------------------------------

``$ http POST ':24817'$REMOTE_HREF'sync/' repository=$REPO_HREF mirror=True``

Look at the new Repository Version created
------------------------------------------

``$ http GET ':24817'$REPO_HREF'versions/1/'``

.. code:: json

    {
        "_created": "2019-05-05T13:41:47.434490Z",
        "_href": "/pulp/api/v3/repositories/696c8cf3-3ad6-4af9-a007-e6c43272df94/versions/1/",
        "base_version": null,
        "content_summary": {
            "added": {
                "file.file": {
                    "count": 3,
                    "href": "/pulp/api/v3/content/file/files/?repository_version_added=/pulp/api/v3/repositories/696c8cf3-3ad6-4af9-a007-e6c43272df94/versions/1/"
                }
            },
            "present": {
                "file.file": {
                    "count": 3,
                    "href": "/pulp/api/v3/content/file/files/?repository_version=/pulp/api/v3/repositories/696c8cf3-3ad6-4af9-a007-e6c43272df94/versions/1/"
                }
            },
            "removed": {}
        },
        "number": 1
    }


Upload ``foo.tar.gz`` to Pulp
-----------------------------

Create an Artifact by uploading the file to Pulp.

``$ http --form POST http://localhost:24817/pulp/api/v3/artifacts/ file@./foo.tar.gz``

.. code:: json

    {
        "_href": "/pulp/api/v3/artifacts/54997c3a-9dc6-4319-bdb8-206bd2fc469e/",
        ...
    }


Create ``file`` content from an Artifact
-----------------------------------------

Create a content unit and point it to your artifact (use the `_href` field you obtained when creating the artifact)

``$ http POST http://localhost:24817/pulp/api/v3/content/file/files/ relative_path=foo.tar.gz _artifact="/pulp/api/v3/artifacts/54997c3a-9dc6-4319-bdb8-206bd2fc469e/"``

.. code:: json

    {
        "_artifact": "/pulp/api/v3/artifacts/54997c3a-9dc6-4319-bdb8-206bd2fc469e/",
        "_created": "2019-05-05T13:47:18.519243Z",
        "_href": "/pulp/api/v3/content/file/files/6a334efb-e59b-42ab-8fa9-cc706d85af25/",
        "_type": "file.file",
        "relative_path": "foo.tar.gz"
    }

``$ export CONTENT_HREF=$(http :24817/pulp/api/v3/content/file/files/ | jq -r '.results[] | select(.relative_path == "foo.tar.gz") | ._href')``


Add content to repository ``foo``
---------------------------------

``$ http POST ':24817'$REPO_HREF'versions/' add_content_units:="[\"$CONTENT_HREF\"]"``


Create a Publication
--------------------

``$ http POST http://localhost:24817/pulp/api/v3/publications/file/file/ repository=$REPO_HREF``

.. code:: json

    {
        "task": "/pulp/api/v3/tasks/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/"
    }

``$ export PUBLICATION_HREF=$(http :24817/pulp/api/v3/publications/file/file/ | jq -r '.results[0] | ._href')``

Create a Distribution for the Publication
-----------------------------------------

``$ http POST http://localhost:24817/pulp/api/v3/distributions/file/file/ name='baz' base_path='foo' publication=$PUBLICATION_HREF``


Download ``foo.tar.gz`` from Pulp
---------------------------------

``$ http GET http://localhost:24816/pulp/content/foo/foo.tar.gz``
