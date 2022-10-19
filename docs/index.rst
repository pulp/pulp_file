``pulp_file`` Plugin
====================

This is the ``pulp_file`` Plugin for `Pulp Project
3.0+ <https://pypi.org/project/pulpcore/>`__. This plugin replaces the ISO support in the
``pulp_rpm`` plugin for Pulp 2.

Overview
--------

A ``pulp_file`` repository consists of a list of arbitrary files, along with a ``PULP_MANIFEST`` file.
The ``PULP_MANIFEST`` consists of one line per file, each line with the format
``filename,sha256-checksum,size-in-bytes`` .

If you follow the :doc:`workflows/upload` and :doc:`workflows/publish-host` workflows, Pulp will create a
``PULP_MANIFEST`` for a repository at Publish-time.

If you are setting up a directory that you wish to make available to Pulp to synchronize, it will need
to have its own ``PULP_MANIFEST``. You can take advantage of the
`pulp-manifest tool <https://github.com/pulp/pulp-manifest/>`_ to create one for you from an existing directory
of files to be served.

How to use these docs
---------------------

The documentation here should be considered **the primary documentation for managing File
content**.

All relevent workflows are covered here, with references to pulpcore supplemental docs. Users may
also find `pulpcore's conceptual docs <https://docs.pulpproject.org/pulpcore/concepts.html>`_
helpful. Here, the documentation falls into two main categories:

  1. :ref:`workflows-index` show the **major features** of the File plugin, with links to reference
     docs.
  2. `REST API Docs <restapi.html>`_ are automatically generated and are responsible for containing
     thorough information for each **minor feature**, including all fields and options.

Community
---------

This plugin exists to serve the community. If we can do more for your use case, please let us know!
Also, contributions are greatly appreciated in the form of:

  1. `Github Issues <https://github.com/pulp/pulp_file/issues>`_
  2. `Github Pull Requests <https://github.com/pulp/pulp_file>`_
  3. `Helping other users <https://pulpproject.org/get_involved/>`_

We can usually be found on Matrix in `pulp-dev` and `pulp` rooms.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 1

   installation
   workflows/index
   restapi/index
   role-based-access-control
   changes
   contributing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
