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

1.12.0 (2023-02-03)
===================


Features
--------

- Added a permission check on the used upload in the single shot content creation call.
  `#747 <https://github.com/pulp/pulp_file/issues/747>`__
- The upload feature was changed to accept already existing file content. This allows multiple users to own identical files.
  `#774 <https://github.com/pulp/pulp_file/issues/774>`__
- Allowed users to publish without manifests by settings the ``manifest`` field to null.
  `#837 <https://github.com/pulp/pulp_file/issues/837>`__
- Added a feature that allows Pulp to automatically create missing repositories on import.
  `#866 <https://github.com/pulp/pulp_file/issues/866>`__


Improved Documentation
----------------------

- Added an overview section, with a pointer to the pulp-manifest tool.
  `#844 <https://github.com/pulp/pulp_file/issues/844>`__


Misc
----

- `#813 <https://github.com/pulp/pulp_file/issues/813>`__, `#814 <https://github.com/pulp/pulp_file/issues/814>`__, `#815 <https://github.com/pulp/pulp_file/issues/815>`__, `#816 <https://github.com/pulp/pulp_file/issues/816>`__, `#818 <https://github.com/pulp/pulp_file/issues/818>`__, `#819 <https://github.com/pulp/pulp_file/issues/819>`__, `#820 <https://github.com/pulp/pulp_file/issues/820>`__, `#821 <https://github.com/pulp/pulp_file/issues/821>`__, `#822 <https://github.com/pulp/pulp_file/issues/822>`__, `#823 <https://github.com/pulp/pulp_file/issues/823>`__, `#824 <https://github.com/pulp/pulp_file/issues/824>`__, `#825 <https://github.com/pulp/pulp_file/issues/825>`__, `#826 <https://github.com/pulp/pulp_file/issues/826>`__, `#828 <https://github.com/pulp/pulp_file/issues/828>`__, `#862 <https://github.com/pulp/pulp_file/issues/862>`__, `#867 <https://github.com/pulp/pulp_file/issues/867>`__, `#876 <https://github.com/pulp/pulp_file/issues/876>`__, `#881 <https://github.com/pulp/pulp_file/issues/881>`__


----


1.11.3 (2023-01-27)
===================


No significant changes.


----


1.11.2 (2022-10-18)
===================


No significant changes.


----


1.11.1 (2022-08-01)
===================


No significant changes.


----


1.11.0 (2022-07-28)
===================


Features
--------

- Added Role Based Access Control for each endpoint.
  * New default roles (creator, owner, viewer) have been added for ``FileRepository``, ``FileRemote``,
  ``FileDistribution``, ``FilePublication``, and ``FileAlternateContentSource``.
  * New detail role management endpoints (``my_permissions``, ``list_roles``, ``add_role``,
  ``remove_role``) have been added to each endpoint.
  `#626 <https://github.com/pulp/pulp_file/issues/626>`__
- File Content is now scoped based on repositories the user has permission to see.
  `#724 <https://github.com/pulp/pulp_file/issues/724>`__
- Added new condition on file uploads to require ``repository`` field if user is not an admin.
  `#729 <https://github.com/pulp/pulp_file/issues/729>`__


Bugfixes
--------

- Improved the error message shown when a user specifies an invalid path to the manifest file, or the manifest file is in the incorrect format.
  `#605 <https://github.com/pulp/pulp_file/issues/605>`__
- The relative_path field of PULP_MANIFEST can now contain commas, since they are valid filename characters in both Linux and Windows filesystems.
  `#630 <https://github.com/pulp/pulp_file/issues/630>`__
- Fixed a bug where publish used /tmp/ instead of the worker working directory.
  `#676 <https://github.com/pulp/pulp_file/issues/676>`__


Misc
----

- `#691 <https://github.com/pulp/pulp_file/issues/691>`__


----


1.10.5 (2022-08-16)
===================


No significant changes.


----


1.10.4 (2022-08-15)
===================


No significant changes.


----


1.10.3 (2022-06-22)
===================


No significant changes.


----


1.10.2 (2022-02-23)
===================


Bugfixes
--------

- Fixed packaging bug which didn't allow pulp_file 1.10 to be installed with pulpcore 3.18.0.
  `#645 <https://pulp.plan.io/issues/645>`_


----


1.10.1 (2021-11-02)
===================


No significant changes.


----


1.10.0 (2021-10-06)
===================


Features
--------

- Added in validation of ACS paths.
  `#9341 <https://pulp.plan.io/issues/9341>`_
- Added refresh endpoint for Alternate Content Sources.
  `#9377 <https://pulp.plan.io/issues/9377>`_
- Enabled remote type validation for the ACS.
  `#9384 <https://pulp.plan.io/issues/9384>`_


Bugfixes
--------

- Fixed bug where sync tasks would open a lot of DB connections.
  `#9252 <https://pulp.plan.io/issues/9252>`_
- Fixed bug where user hidden repos were visible to the user.
  `#9416 <https://pulp.plan.io/issues/9416>`_
- Check whether ACS exists before refreshing it.
  `#9420 <https://pulp.plan.io/issues/9420>`_


Improved Documentation
----------------------

- Updated ACS docs to use CLI.
  `#9373 <https://pulp.plan.io/issues/9373>`_


Misc
----

- `#9357 <https://pulp.plan.io/issues/9357>`_, `#9426 <https://pulp.plan.io/issues/9426>`_


----


1.9.1 (2021-08-30)
==================


Bugfixes
--------

- Fixed bug where sync tasks would open a lot of DB connections.
  (backported from #9252)
  `#9311 <https://pulp.plan.io/issues/9311>`_


----


1.9.0 (2021-08-26)
==================


Features
--------

- Enable reclaim disk feature provided by pulpcore. This feature is available with pulpcore 3.15+.
  `#9168 <https://pulp.plan.io/issues/9168>`_


Bugfixes
--------

- Fix an issue where "mirror=True" syncs of a repository which has already been synced, and has not changed since the last sync, would fail.
  `#8999 <https://pulp.plan.io/issues/8999>`_
- Fixed failing 0012_delete_filefilesystemexporter migration which errors if there are
  ``FileFilesystemExporters``.
  `#9102 <https://pulp.plan.io/issues/9102>`_
- Fixed filtering content by sha256 for on-demand content.
  `#9117 <https://pulp.plan.io/issues/9117>`_


Deprecations and Removals
-------------------------

- Dropped support for Python 3.6 and 3.7. pulp_file now supports Python 3.8+.
  `#9037 <https://pulp.plan.io/issues/9037>`_


Misc
----

- `#8959 <https://pulp.plan.io/issues/8959>`_, `#9154 <https://pulp.plan.io/issues/9154>`_


----


1.8.2 (2021-07-21)
==================


Bugfixes
--------

- Fix an issue where "mirror=True" syncs of a repository which has already been synced, and has not changed since the last sync, would fail.
  (backported from #8999)
  `#9060 <https://pulp.plan.io/issues/9060>`_
- Fixed failing 0012_delete_filefilesystemexporter migration which errors if there are
  ``FileFilesystemExporters``.
  (backported from #9102)
  `#9122 <https://pulp.plan.io/issues/9122>`_


----


1.8.1 (2021-07-01)
==================

Misc
----

- `#8969 <https://pulp.plan.io/issues/8969>`_


----


1.8.0 (2021-06-11)
==================

Features
--------

- Auto-publish no longer modifies distributions.
  Auto-distribute now only requires setting a distribution's ``repository`` field.
  `#8762 <https://pulp.plan.io/issues/8762>`_
- Performing a sync with "mirror=True" will automatically generate a publication at sync-time.
  `#8851 <https://pulp.plan.io/issues/8851>`_


Deprecations and Removals
-------------------------

- The filesystem export functionality has been removed from pulp_file. Users should now use the
  filesystem export functionaliy in pulpcore instead. Upgrading to pulp_file 1.8.0 will drop any
  ``FilesystemExporters`` in pulp_file.
  `#8861 <https://pulp.plan.io/issues/8861>`_


Misc
----

- `#8719 <https://pulp.plan.io/issues/8719>`_


----


1.7.0 (2021-04-16)
==================


Features
--------

- Add support for automatic publishing and distributing.
  `#7469 <https://pulp.plan.io/issues/7469>`_


Improved Documentation
----------------------

- Documented the auto-publication and auto-distribution feature.
  `#8548 <https://pulp.plan.io/issues/8548>`_


Misc
----

- `#8387 <https://pulp.plan.io/issues/8387>`_, `#8415 <https://pulp.plan.io/issues/8415>`_, `#8508 <https://pulp.plan.io/issues/8508>`_


----


1.6.1 (2021-03-30)
==================


Bugfixes
--------

- Added asynchronous tasking to the Update and Delete endpoints of FilesystemExporter to provide proper locking on resources.
  `#8451 <https://pulp.plan.io/issues/8451>`_


Deprecations and Removals
-------------------------

- Update and Delete endpoints of FilesystemExporter changed to return 202 with tasks.
  `#8451 <https://pulp.plan.io/issues/8451>`_


----


1.6.0 (2021-03-05)
==================


Bugfixes
--------

- Fixed a bug which caused the plugin to report the default manifest's name instead of the specified
  one in the publication endpoint.
  `#7838 <https://pulp.plan.io/issues/7838>`_


Improved Documentation
----------------------

- Update workflow docs to pulp-cli.
  `#7530 <https://pulp.plan.io/issues/7530>`_
- Add demo requirement to the Contributing process.
  `#7704 <https://pulp.plan.io/issues/7704>`_
- Update docs link in README.
  `#7932 <https://pulp.plan.io/issues/7932>`_
- Use the ReadTheDocs theme for pulp_file docs.
  `#8165 <https://pulp.plan.io/issues/8165>`_


----


1.5.0 (2020-12-15)
==================


No significant changes. Addressed pulpcore 3.9 deprecations.


----


1.4.0 (2020-12-02)
==================


Bugfixes
--------

- Added some missing files to MANIFEST.in.
  `#7685 <https://pulp.plan.io/issues/7685>`_


Improved Documentation
----------------------

- Documented that a functional test is now a requirement for a feature or a bug fix.
  `#7437 <https://pulp.plan.io/issues/7437>`_


----


1.3.0 (2020-09-23)
==================


Bugfixes
--------

- Fixed exception when hitting ``/pulp/api/v3/exporters/file/filesystem/<uuid>/exports/``.
  `#7522 <https://pulp.plan.io/issues/7522>`_


Improved Documentation
----------------------

- Added docs for using FileSystemExporter.
  `#7515 <https://pulp.plan.io/issues/7515>`_


Misc
----

- `#7454 <https://pulp.plan.io/issues/7454>`_


----


1.2.0 (2020-08-13)
==================


Features
--------

- Added ability for users to add Remote to Repository and automatically use it when syncing.
  `#7135 <https://pulp.plan.io/issues/7135>`_


Improved Documentation
----------------------

- Fixed the name of the artifact field
  `#5966 <https://pulp.plan.io/issues/5966>`_


Misc
----

- `#6936 <https://pulp.plan.io/issues/6936>`_


----


1.1.0 (2020-07-08)
==================


Bugfixes
--------

- Including requirements.txt on MANIFEST.in
  `#6885 <https://pulp.plan.io/issues/6885>`_


Improved Documentation
----------------------

- Added a remainder about the recommended utilities used in the workflows.
  `#5998 <https://pulp.plan.io/issues/5998>`_
- Updated fixture links from fedorapeople.org to fixtures.pulpproject.org.
  `#6653 <https://pulp.plan.io/issues/6653>`_


----


1.0.1 (2020-06-03)
==================


Bugfixes
--------

- Including requirements.txt on MANIFEST.in
  `#6885 <https://pulp.plan.io/issues/6885>`_


----


1.0.0 (2020-05-27)
==================


Misc
----

- `#6514 <https://pulp.plan.io/issues/6514>`_, `#6708 <https://pulp.plan.io/issues/6708>`_, `#6730 <https://pulp.plan.io/issues/6730>`_, `#6761 <https://pulp.plan.io/issues/6761>`_


----


0.3.0 (2020-04-16)
==================


Features
--------

- Added history for filesystem exports at ``/exporters/file/filesystem/<uuid>/exports/``.
  `#6328 <https://pulp.plan.io/issues/6328>`_
- Add support for import/export processing
  `#6472 <https://pulp.plan.io/issues/6472>`_


Deprecations and Removals
-------------------------

- The fileystem exporter endpoint has been moved from ``/exporters/file/file/`` to
  ``/exporters/file/filesystem/`` and the export endpoint is now at POST
  ``/exporters/file/filesystem/<uuid>/exports/``. Additionally, the table is being dropped and
  recreated due to a data structure change in core so users will lose any filesystem exporter data on
  upgrade.
  `#6328 <https://pulp.plan.io/issues/6328>`_


Misc
----

- `#6155 <https://pulp.plan.io/issues/6155>`_, `#6300 <https://pulp.plan.io/issues/6300>`_, `#6362 <https://pulp.plan.io/issues/6362>`_, `#6392 <https://pulp.plan.io/issues/6392>`_


----


0.2.0 (2020-02-26)
==================


Deprecations and Removals
-------------------------

- Renamed the filter for the field 'digest' to 'sha256' to correspond to field name in API and other
  plugins.
  `#5965 <https://pulp.plan.io/issues/5965>`_


Misc
----

- `#5567 <https://pulp.plan.io/issues/5567>`_


----


0.1.1 (2020-01-31)
==================


Bugfixes
--------

- Adjusts setup.py classifier to show 0.1.0 as Production/Stable.
  `#5897 <https://pulp.plan.io/issues/5897>`_


Misc
----

- `#5867 <https://pulp.plan.io/issues/5867>`_, `#5872 <https://pulp.plan.io/issues/5872>`_, `#5967 <https://pulp.plan.io/issues/5967>`_, `#6016 <https://pulp.plan.io/issues/6016>`_


----


0.1.0 (2019-12-12)
==================


Improved Documentation
----------------------

- Labeling Exporters as tech preview.
  `#5563 <https://pulp.plan.io/issues/5563>`_


Misc
----

- `#5701 <https://pulp.plan.io/issues/5701>`_


----


0.1.0rc2 (2019-12-03)
=====================


Features
--------

- Add checking for path overlapping for RepositoryVersions and Publications.
  `#5559 <https://pulp.plan.io/issues/5559>`_


Misc
----

- `#5757 <https://pulp.plan.io/issues/5757>`_


----


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


