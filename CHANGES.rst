=========
Changelog
=========

..
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://docs.pulpproject.org/en/3.0/nightly/contributing/git.html#changelog-update

    WARNING: Don't drop the next directive!

.. towncrier release notes start

0.1.0b3 (2019-09-30)
====================


Features
--------

- Setting `code` on `ProgressBar`.
  `#5184 <https://pulp.plan.io/issues/5184>`_
- Add upload functionality to the file content endpoint.
  `#5403 <https://pulp.plan.io/issues/5403>`_


Deprecations and Removals
-------------------------

- Adjust FileContentSerializer to upstream change.
  `#5428 <https://pulp.plan.io/issues/5428>`_


Misc
----

- `#5304 <https://pulp.plan.io/issues/5304>`_, `#5444 <https://pulp.plan.io/issues/5444>`_


----


0.1.0b2 (2019-09-11)
====================


Improved Documentation
----------------------

- Fix the code snippet provided in the example for creating a file content
  `#5094 <https://pulp.plan.io/issues/5094>`_


Misc
----

- `#4681 <https://pulp.plan.io/issues/4681>`_


----


0.1.0b1 (2019-07-09)
====================


Features
--------

- Override the Remote's serializer to allow policy='on_demand' and policy='streamed'.
  `#4990 <https://pulp.plan.io/issues/4990>`_


Improved Documentation
----------------------

- Switch to using `towncrier <https://github.com/hawkowl/towncrier>`_ for better release notes.
  `#4875 <https://pulp.plan.io/issues/4875>`_


