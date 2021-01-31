Scripting
=========

Each workflow renders bash scripts that allow the developers to ensure the continued correctness of
the instructions. These scripts may also be helpful to users as a basis for their own scripts. All
of the scripts can be found at https://github.com/pulp/pulp_file/tree/master/docs/_scripts/

The following scripts are used in conjunction with all the workflow scripts:

**Setup**

.. literalinclude:: ../_scripts/setup.sh
   :language: bash

Correctness Check (Destructive)
-------------------------------

To check the correctness of the sync and publish workflow scripts, they can all be run together using:

.. literalinclude:: ../_scripts/docs_check_sync_publish.sh
   :language: bash

To check the correctness of the upload and publish workflow scripts, they can all be run together using:
script.

.. literalinclude:: ../_scripts/docs_check_upload_publish.sh
   :language: bash
