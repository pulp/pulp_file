.. _workflows-index:

Workflows
=========

This section will document the **major features** of `pulp-file` in a "quickstart" style. More
detailed information (REST API Reference) is linked in each section.

If you have not yet installed Pulp and the File plugin, please follow our :doc:`../installation`.
These documents will assume you have the environment installed and ready to go.

**httpie**

The REST API examples here use `httpie <https://httpie.org/doc>`_ to perform the requests.
The ``httpie`` commands below assume that the user executing the commands has a ``.netrc`` file
in the home directory. The ``.netrc`` should have the following configuration:

.. code-block:: bash

    machine localhost
    login admin
    password password

If you configured the ``admin`` user with a different password, adjust the configuration
accordingly. If you prefer to specify the username and password with each request, please see
``httpie`` documentation on how to do that.

**jq**

This documentation makes use of the `jq library <https://stedolan.github.io/jq/>`_
to parse the json received from requests, in order to get the unique urls generated
when objects are created. To follow this documentation as-is please install the jq
library with:

``$ sudo dnf install jq``

.. toctree::
   :maxdepth: 2

   scripting
   sync
   upload
   publish-host
