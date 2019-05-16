Synchronize a Repository
========================

Create a repository ``foo``
---------------------------

``$ http POST http://localhost:24817/pulp/api/v3/repositories/ name=foo``

.. code:: json

    {
        "_href": "/pulp/api/v3/repositories/696c8cf3-3ad6-4af9-a007-e6c43272df94/",
        ...
    }

``$ export REPO_HREF=$(http :24817/pulp/api/v3/repositories/ | jq -r '.results[] | select(.name == "foo") | ._href')``

Reference (pulpcore): `Repository API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#tag/repositories>`_

Create a new remote ``bar``
---------------------------

``$ http POST http://localhost:24817/pulp/api/v3/remotes/file/file/ name='bar' url='https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST'``

.. code:: json

    {
        "_href": "/pulp/api/v3/remotes/file/file/8098cf53-df95-4889-bb3b-3c10e23063ce/",
        ...
    }

``$ export REMOTE_HREF=$(http :24817/pulp/api/v3/remotes/file/file/ | jq -r '.results[] | select(.name == "bar") | ._href')``

Reference: `File Remote Usage <../restapi.html#tag/remotes>`_

Sync repository ``foo`` using remote ``bar``
--------------------------------------------

``$ http POST ':24817'$REMOTE_HREF'sync/' repository=$REPO_HREF mirror=True``

Reference: `File Sync Usage <../restapi.html#operation/remotes_file_file_sync>`_

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

Reference (pulpcore): `Repository Version API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#operation/repositories_versions_list>`_
