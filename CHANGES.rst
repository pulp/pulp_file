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

0.1.0rc1 (2019-11-14)
=====================


Features
--------

- Sync, Upload, and Modify now have added content with the same `relative_path` as existing content
  will remove the existing content.
  `#3541 <https://pulp.plan.io/issues/3541>`_
- Change `relative_path` from `CharField` to `TextField`
  `#4544 <https://pulp.plan.io/issues/4544>`_
- Added support for exporting file publications to the filesystem.
  `#5086 <https://pulp.plan.io/issues/5086>`_


Deprecations and Removals
-------------------------

- Sync is no longer available at the {remote_href}/sync/ repository={repo_href} endpoint. Instead, use POST {repo_href}/sync/ remote={remote_href}.

  Creating / listing / editing / deleting file repositories is now performed on /pulp/api/v3/file/file/ instead of /pulp/api/v3/repositories/. Only file content can be present in a file repository, and only a file repository can hold file content.
  `#5625 <https://pulp.plan.io/issues/5625>`_


Misc
----

- `#3308 <https://pulp.plan.io/issues/3308>`_, `#5458 <https://pulp.plan.io/issues/5458>`_, `#5580 <https://pulp.plan.io/issues/5580>`_, `#5629 <https://pulp.plan.io/issues/5629>`_


----


0.1.0b4 (2019-10-15)
====================


Bugfixes
--------

- New RepositoryVersions will remove an existing unit at the same `relative_path`. This is true for
  both `sync` and `upload`, and is per Repository.
  `#4028 <https://pulp.plan.io/issues/4028>`_


Improved Documentation
----------------------

- Change the prefix of Pulp services from pulp-* to pulpcore-*
  `#4554 <https://pulp.plan.io/issues/4554>`_


Deprecations and Removals
-------------------------

- Change `_id`, `_created`, `_last_updated`, `_href` to `pulp_id`, `pulp_created`, `pulp_last_updated`, `pulp_href`
  `#5457 <https://pulp.plan.io/issues/5457>`_
- Remove "_" from `_versions_href`, `_latest_version_href`
  `#5548 <https://pulp.plan.io/issues/5548>`_
- Removing base field: `_type` .
  `#5550 <https://pulp.plan.io/issues/5550>`_


----


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


