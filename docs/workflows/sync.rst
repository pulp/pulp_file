Synchronize a Repository
========================

Create a repository ``foo``
---------------------------

.. literalinclude:: ../_scripts/repo.sh
   :language: bash

Repository GET Response::

    {
        "pulp_created": "2019-05-16T19:23:55.224096Z",
        "pulp_href": "/pulp/api/v3/repositories/file/file/680f18e7-0513-461f-b067-436b03285e4c/",
        "latest_version_href": null,
        "versions_href": "/pulp/api/v3/repositories/file/file/680f18e7-0513-461f-b067-436b03285e4c/versions/",
        "description": "",
        "name": "foo"
    }


Reference (pulpcore): `Repository API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#tag/repositories>`_

Create a new remote ``bar``
---------------------------

.. literalinclude:: ../_scripts/remote.sh
   :language: bash

Remote GET Response::

    {
        "pulp_created": "2019-05-16T19:23:56.771326Z",
        "pulp_href": "/pulp/api/v3/remotes/file/file/e682efef-3974-4366-aece-a333bfaec9f3/",
        "pulp_last_updated": "2019-05-16T19:23:56.771341Z",
        "download_concurrency": 20,
        "name": "bar",
        "policy": "immediate",
        "proxy_url": "",
        "ssl_ca_certificate": null,
        "ssl_client_certificate": null,
        "ssl_client_key": null,
        "ssl_validation": true,
        "url": "https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST",
        "validate": true
    }


Reference: `File Remote Usage <../restapi.html#tag/remotes>`_

Sync repository ``foo`` using remote ``bar``
--------------------------------------------

.. literalinclude:: ../_scripts/sync.sh
   :language: bash

Repository Version GET Response (when complete)::

    {
        "pulp_created": "2019-05-16T19:23:58.230896Z",
        "pulp_href": "/pulp/api/v3/repositories/file/file/680f18e7-0513-461f-b067-436b03285e4c/versions/1/",
        "base_version": null,
        "content_summary": {
            "added": {
                "file.file": {
                    "count": 3,
                    "href": "/pulp/api/v3/content/file/files/?repository_version_added=/pulp/api/v3/repositories/file/file/680f18e7-0513-461f-b067-436b03285e4c/versions/1/"
                }
            },
            "present": {
                "file.file": {
                    "count": 3,
                    "href": "/pulp/api/v3/content/file/files/?repository_version=/pulp/api/v3/repositories/file/file/680f18e7-0513-461f-b067-436b03285e4c/versions/1/"
                }
            },
            "removed": {}
        },
        "number": 1
    }

Reference: `File Sync Usage <../restapi.html#operation/remotes_file_file_sync>`_

Reference (pulpcore): `Repository Version API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#operation/repositories_versions_list>`_
