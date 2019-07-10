Upload Content
==============

Upload a file to Pulp (Create an Artifact)
------------------------------------------

.. literalinclude:: ../_scripts/artifact.sh
   :language: bash

Artifact GET Response::

    {
        "_created": "2019-05-16T20:07:48.066089Z",
        "_href": "/pulp/api/v3/artifacts/cff8078a-826f-4f7e-930d-422c2f134a07/",
        "file": "artifact/97/144ab16c9aa0e6072d471d6aebe7c21083e21359137e676445bfeb4051ba25",
        "md5": "5148c996f375ed5aab94ef6993df90a0",
        "sha1": "a7bd2bcaf1d68505f3e8b2cfe3505d01b31db306",
        "sha224": "18a167922b68a3fb8f2d9a71fa78f9776f5402dce4b3d97d5cea2559",
        "sha256": "97144ab16c9aa0e6072d471d6aebe7c21083e21359137e676445bfeb4051ba25",
        "sha384": "4cd006bfac7f2e41baa8c411536579b134daeb3ad666310d21463f384a7020360703fc5538b4eca724033498d514e144",
        "sha512": "e1aae6bbc6fd24cf890b82ffa824629518e6e93935935a0b7c008fbd9fa59f08aa32a7d8580b31a65b21caa0f48e737d8e555eaa777912bea5772799f64a2dd4",
        "size": 11
    }

Reference (pulpcore): `Artifact API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#tag/artifacts>`_

Create ``file`` content from an Artifact
-----------------------------------------

.. literalinclude:: ../_scripts/content.sh
   :language: bash

Content GET Response::

    {
        "_artifact": "/pulp/api/v3/artifacts/cff8078a-826f-4f7e-930d-422c2f134a07/",
        "_created": "2019-05-16T20:07:48.929374Z",
        "_href": "/pulp/api/v3/content/file/files/c23def43-44bc-45f4-8a6f-0310285f5339/",
        "_type": "file.file",
        "relative_path": "test_upload.txt"
    }

Reference: `File Content API Usage <../restapi.html#tag/content>`_

Create a repository ``foo``
---------------------------

.. literalinclude:: ../_scripts/repo.sh
   :language: bash

Repository GET Response::

    {
        "_created": "2019-05-16T19:23:55.224096Z",
        "_href": "/pulp/api/v3/repositories/680f18e7-0513-461f-b067-436b03285e4c/",
        "_latest_version_href": null,
        "_versions_href": "/pulp/api/v3/repositories/680f18e7-0513-461f-b067-436b03285e4c/versions/",
        "description": "",
        "name": "foo"
    }


Reference (pulpcore): `Repository API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#tag/repositories>`_

Add content to repository ``foo``
---------------------------------

.. literalinclude:: ../_scripts/add_remove.sh
   :language: bash

Repository Version GET Response::

    {
        "_created": "2019-05-16T20:07:50.363735Z",
        "_href": "/pulp/api/v3/repositories/0d908664-e300-4223-869b-fc5d2cef285f/versions/1/",
        "base_version": null,
        "content_summary": {
            "added": {
                "file.file": {
                    "count": 1,
                    "href": "/pulp/api/v3/content/file/files/?repository_version_added=/pulp/api/v3/repositories/0d908664-e300-4223-869b-fc5d2cef285f/versions/1/"
                }
            },
            "present": {
                "file.file": {
                    "count": 1,
                    "href": "/pulp/api/v3/content/file/files/?repository_version=/pulp/api/v3/repositories/0d908664-e300-4223-869b-fc5d2cef285f/versions/1/"
                }
            },
            "removed": {}
        },
        "number": 1
    }

Reference (pulpcore): `Repository Version Creation API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#operation/repositories_versions_create>`_
