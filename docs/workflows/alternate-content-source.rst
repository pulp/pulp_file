Alternate Content Sources
=========================

To use an Alternate Content Source you need a ``FileRemote`` with base path of your
ACS.

.. code-block:: bash

    http POST localhost:24817/pulp/api/v3/remotes/file/file/ name="remoteForACS" policy="on_demand" url="http://fixtures.pulpproject.org/"

Create Alternate Content Source
-------------------------------

.. code-block:: bash

    http POST localhost:24817/pulp/api/v3/acs/file/file/ name="fileAcs" remote=<pulp-remote-href> paths:='["file/PULP_MANIFEST", "backup/MANIFEST"]'

Refresh ACS
-----------

To make your ACS available for future syncs you need to call ``refresh`` endpoint
on your ACS.

.. code-block:: bash

    http POST localhost:24817/pulp/api/v3/acs/file/file/<ACS-UUID>/refresh/

Alternate Content Source has a global scope so if any content is found in ACS it
will be used in all future syncs.
