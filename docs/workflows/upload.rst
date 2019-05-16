Upload Content
==============

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

Reference: `File Content API Usage <../restapi.html#tag/content>`_

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


Add content to repository ``foo``
---------------------------------

``$ http POST ':24817'$REPO_HREF'versions/' add_content_units:="[\"$CONTENT_HREF\"]"``

Reference (pulpcore): `Repository Version Creation API Usage
<https://docs.pulpproject.org/en/3.0/nightly/restapi.html#operation/repositories_versions_create>`_
