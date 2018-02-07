``pulp_file`` Plugin
=======================

This is the ``pulp_file`` Plugin for `Pulp Project
3.0+ <https://pypi.python.org/pypi/pulpcore/>`__. This plugin replaces the ISO support in the
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

Install ``pulp-file`` from source
---------------------------------

1)  sudo -u pulp -i
2)  source ~/pulpvenv/bin/activate
3)  git clone https://github.com/pulp/pulp\_file.git
4)  cd pulp\_file
5)  python setup.py develop
6)  pulp-manager makemigrations pulp\_file
7)  pulp-manager migrate pulp\_file
8)  django-admin runserver
9)  sudo systemctl restart pulp\_resource\_manager
10) sudo systemctl restart pulp\_worker@1
11) sudo systemctl restart pulp\_worker@2

Install ``pulp-file`` From PyPI
-------------------------------

1) sudo -u pulp -i
2) source ~/pulpvenv/bin/activate
3) pip install pulp-file
4) pulp-manager makemigrations pulp\_file
5) pulp-manager migrate pulp\_file
6) django-admin runserver
7) sudo systemctl restart pulp\_resource\_manager
8) sudo systemctl restart pulp\_worker@1
9) sudo systemctl restart pulp\_worker@2

Create a repository ``foo``
---------------------------

``$ http POST http://localhost:8000/api/v3/repositories/ name=foo``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/repositories/8d7cd67a-9421-461f-9106-2df8e4854f5f/",
        ...
    }

``$ export REPO_HREF=$(http :8000/api/v3/repositories/ | jq -r '.results[] | select(.name == "foo") | ._href')``

Add an importer to repository ``foo``
-------------------------------------

``$ http POST http://localhost:8000/api/v3/importers/file/ name='bar' download_policy='immediate' sync_mode='mirror' feed_url='https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST' repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/importers/file/13ac2d63-7b7b-401d-b71b-9a5af05aab3c/",
        ...
    }

``$ export IMPORTER_HREF=$(http :8000/api/v3/importers/file/ | jq -r '.results[] | select(.name == "bar") | ._href')``

Sync repository ``foo`` using importer ``bar``
----------------------------------------------

``$ http POST $IMPORTER_HREF'sync/' repository=$REPO_HREF``

Upload ``foo.tar.gz`` to Pulp
-----------------------------

Create an Artifact by uploading the file to Pulp.

``$ http --form POST http://localhost:8000/api/v3/artifacts/ file@./foo.tar.gz``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/",
        ...
    }

Create ``file`` content from an Artifact
-------------------------------------------

Create a file with the json bellow and save it as content.json.

.. code:: json

    {
      "digest": "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c",
      "path": "foo.tar.gz",
      "artifacts": {"foo.tar.gz":"http://localhost:8000/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/"}
    }

``$ http POST http://localhost:8000/api/v3/content/file/ < content.json``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/content/file/a9578a5f-c59f-4920-9497-8d1699c112ff/",
        "artifacts": {
            "foo.tar.gz": "http://localhost:8000/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/"
        },
        "digest": "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c",
        "notes": {},
        "path": "foo.tar.gz",
        "type": "file"
    }

``$ export CONTENT_HREF=$(http :8000/api/v3/content/file/ | jq -r '.results[] | select(.path == "foo.tar.gz") | ._href')``


Add content to repository ``foo``
---------------------------------

Currently there is no endpoint to manually associate content to a repository. This functionality
will be added before pulp3 beta is released.

Add a ``file`` Publisher to repository ``foo``
--------------------------------------------------

``$ http POST http://localhost:8000/api/v3/publishers/file/ name=bar repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/publishers/file/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/",
        ...
    }

``$ export PUBLISHER_HREF=$(http :8000/api/v3/publishers/file/ | jq -r '.results[] | select(.name == "bar") | ._href')``


Use the ``bar`` Publisher to create a Publication
-------------------------------------------------
``$ http POST $PUBLISHER_HREF'publish/' repository=$REPO_HREF``

.. code:: json

    [
        {
            "_href": "http://localhost:8000/api/v3/tasks/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/",
            "task_id": "fd4cbecd-6c6a-4197-9cbe-4e45b0516309"
        }
    ]

``$ export PUBLICATION_HREF=$(http :8000/api/v3/publications/ | jq -r --arg PUBLISHER_HREF "$PUBLISHER_HREF" '.results[] | select(.publisher==$PUBLISHER_HREF) | ._href')``

Add a Distribution to Publisher ``bar``
---------------------------------------

``$ http POST http://localhost:8000/api/v3/distributions/ name='baz' base_path='foo' auto_updated=true http=true https=true publisher=$PUBLISHER_HREF publication=$PUBLICATION_HREF``


.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/distributions/9b29f1b2-6726-40a2-988a-273d3f009a41/",
       ...
    }



Check status of a task
----------------------

``$ http GET http://localhost:8000/api/v3/tasks/82e64412-47f8-4dd4-aa55-9de89a6c549b/``

Download ``test.iso`` from Pulp
---------------------------------

``$ http GET http://localhost:8000/content/foo/test.iso``
