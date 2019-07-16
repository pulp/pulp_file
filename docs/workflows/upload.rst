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
        "md5": "3b4fd267e71a1a8e8746893fcc91e5b5",
        "relative_path": "test_upload.txt",
        "sha1": "6fd76062f3680be44de9ed6a4b80bdce512dd620",
        "sha224": "3b518d0e428c4e5996ec6861960a7640770bc8bbbe16775b1dfc1e81",
        "sha256": "b671500c402128babf4f4e51afc552584df3db501bb1a0bd3ee96dc121228a9c",
        "sha384": "7f90e3b612defd1d85d51c3a0efca932fb1a6cdee4a11dd532edd8302dfe7860d3ce4d50b2ed73d984a83e6c6265e54b",
        "sha512": "91c823e2d547e4073d4c47f73f36122acf60a722100d6e592a68aae0b6ba8ee12cd40dbed75cade7ad1a1f7e197a06ed2ad184da8c0055b5473bcf07aaf7e44c"
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
        "description": null,
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
