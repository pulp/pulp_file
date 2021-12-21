Contributing
============

To contribute to the ``pulp_file`` package follow this process:

1. Clone the GitHub repo
2. Make a change
3. Add a functional test for the change
4. Make sure all tests pass
5. Add a file into CHANGES folder (:ref:`changelog-update`).
6. Commit changes to your own ``pulp_file`` clone
7. `Record a demo <https://docs.pulpproject.org/pulpcore/en/master/nightly/contributing/record-a-demo.html>` (1-3 minutes).
8. Make a pull request on the GitHub page for your clone against master branch


.. _changelog-update:

Changelog update
****************

The CHANGES.rst file is managed using the `towncrier tool <https://github.com/hawkowl/towncrier>`_
and all non trivial changes must be accompanied by a news entry.

To add an entry to the news file, you first need an issue in github describing the change you
want to make. Once you have an issue, take its number and create a file inside of the ``CHANGES/``
directory named after that issue number with an extension of .feature, .bugfix, .doc, .removal, or
.misc. So if your issue is 3543 and it fixes a bug, you would create the file
``CHANGES/3543.bugfix``.

PRs can span multiple categories by creating multiple files (for instance, if you added a feature
and deprecated an old feature at the same time, you would create CHANGES/NNNN.feature and
CHANGES/NNNN.removal). Likewise if a PR touches multiple issues/PRs you may create a file for each
of them with the exact same contents and Towncrier will deduplicate them.

The contents of this file are reStructuredText formatted text that will be used as the content of
the news file entry. You do not need to reference the issue or PR numbers here as towncrier will
automatically add a reference to all of the affected issues when rendering the news file.
