Alternate Content Sources
=========================

To use an Alternate Content Source you need a ``FileRemote`` with base path of your
ACS.

.. code-block:: bash

    pulp file remote create --name remoteForACS --policy on_demand --url https://fixtures.pulpproject.org/file-manifest/PULP_MANIFEST

Create Alternate Content Source
-------------------------------

.. code-block:: bash

    pulp file acs create --name fileAcs --remote remoteForACS --path "file/PULP_MANIFEST" --path "file2/PULP_MANIFEST"

Refresh ACS
-----------

To make your ACS available for future syncs you need to call ``refresh`` on your ACS.

.. code-block:: bash

    pulp file acs refresh --name fileAcs

Alternate Content Sources have a global scope so if any content is found in ACS it will be used in
all future syncs.
