# Changelog

[//]: # (You should *NOT* be adding new change log entries to this file, this)
[//]: # (file is managed by towncrier. You *may* edit previous change logs to)
[//]: # (fix problems like typo corrections or such.)
[//]: # (To add a new change log entry, please see the contributing docs.)
[//]: # (WARNING: Don't drop the towncrier directive!)

[//]: # (towncrier release notes start)

## 1.16.0 (2023-11-10) {: #1.16.0 }

### Deprecations and Removals

-   This is the last release of `pulp_file` as an independent package.
    Its bits have been moved to `pulpcore>=3.40.0` and this is essentially an empty package.
    You can safely remove it.
    [#+final_release_note](https://github.com/pulp/pulp_file/issues/+final_release_note)

---

## 1.15.1 (2023-10-27) {: #1.15.1 }

No significant changes.

---

## 1.15.0 (2023-10-19) {: #1.15.0 }

### Features

-   Adjusted default access policies for new labels API.
    [#1039](https://github.com/pulp/pulp_file/issues/1039)

### Bugfixes

-   Allows for compatibility with pulpcore>3.25.
    [#954](https://github.com/pulp/pulp_file/issues/954)

### Misc

-   [#804](https://github.com/pulp/pulp_file/issues/804)

---

## 1.14.5 (2023-09-26) {: #1.14.5 }

No significant changes.

---

## 1.14.4 (2023-08-17) {: #1.14.4 }

No significant changes.

---

## 1.14.3 (2023-05-11) {: #1.14.3 }

No significant changes.

---

## 1.14.2 (2023-05-04) {: #1.14.2 }

### Bugfixes

-   Allows for compatibility with pulpcore>3.25.
    [#954](https://github.com/pulp/pulp_file/issues/954)

---

## 1.14.1 (2023-04-18) {: #1.14.1 }

No significant changes.

---

## 1.14.0 (2023-04-04) {: #1.14.0 }

### Features

-   Added the ability to replicate File distributions/repositories from an upstream Pulp instance.
    [#909](https://github.com/pulp/pulp_file/issues/909)

### Misc

-   [#933](https://github.com/pulp/pulp_file/issues/933)

---

## 1.13.1 (2023-03-23) {: #1.13.1 }

No significant changes.

---

## YANKED 1.13.0 (2023-03-14) {: #1.13.0 }

Yank reason: incorrect peer dependencies

### Features

-   Added Domains compatibility.
    [#859](https://github.com/pulp/pulp_file/issues/859)

---

## 1.12.0 (2023-02-03) {: #1.12.0 }

### Features

-   Added a permission check on the used upload in the single shot content creation call.
    [#747](https://github.com/pulp/pulp_file/issues/747)
-   The upload feature was changed to accept already existing file content. This allows multiple users to own identical files.
    [#774](https://github.com/pulp/pulp_file/issues/774)
-   Allowed users to publish without manifests by settings the `manifest` field to null.
    [#837](https://github.com/pulp/pulp_file/issues/837)
-   Added a feature that allows Pulp to automatically create missing repositories on import.
    [#866](https://github.com/pulp/pulp_file/issues/866)

### Improved Documentation

-   Added an overview section, with a pointer to the pulp-manifest tool.
    [#844](https://github.com/pulp/pulp_file/issues/844)

### Misc

-   [#813](https://github.com/pulp/pulp_file/issues/813), [#814](https://github.com/pulp/pulp_file/issues/814), [#815](https://github.com/pulp/pulp_file/issues/815), [#816](https://github.com/pulp/pulp_file/issues/816), [#818](https://github.com/pulp/pulp_file/issues/818), [#819](https://github.com/pulp/pulp_file/issues/819), [#820](https://github.com/pulp/pulp_file/issues/820), [#821](https://github.com/pulp/pulp_file/issues/821), [#822](https://github.com/pulp/pulp_file/issues/822), [#823](https://github.com/pulp/pulp_file/issues/823), [#824](https://github.com/pulp/pulp_file/issues/824), [#825](https://github.com/pulp/pulp_file/issues/825), [#826](https://github.com/pulp/pulp_file/issues/826), [#828](https://github.com/pulp/pulp_file/issues/828), [#862](https://github.com/pulp/pulp_file/issues/862), [#867](https://github.com/pulp/pulp_file/issues/867), [#876](https://github.com/pulp/pulp_file/issues/876), [#881](https://github.com/pulp/pulp_file/issues/881)

---

## 1.11.3 (2023-01-27) {: #1.11.3 }

No significant changes.

---

## 1.11.2 (2022-10-18) {: #1.11.2 }

No significant changes.

---

## 1.11.1 (2022-08-01) {: #1.11.1 }

No significant changes.

---

## YANKED 1.11.0 (2022-07-28) {: #1.11.0 }

Yank reason: Declared package compatibility is incorrect

### Features

-   Added Role Based Access Control for each endpoint.

    * New default roles (creator, owner, viewer) have been added for `FileRepository`, `FileRemote`,
    `FileDistribution`, `FilePublication`, and `FileAlternateContentSource`.

    * New detail role management endpoints (`my_permissions`, `list_roles`, `add_role`,
    `remove_role`) have been added to each endpoint.
    [#626](https://github.com/pulp/pulp_file/issues/626)

-   File Content is now scoped based on repositories the user has permission to see.
    [#724](https://github.com/pulp/pulp_file/issues/724)

-   Added new condition on file uploads to require `repository` field if user is not an admin.
    [#729](https://github.com/pulp/pulp_file/issues/729)

### Bugfixes

-   Improved the error message shown when a user specifies an invalid path to the manifest file, or the manifest file is in the incorrect format.
    [#605](https://github.com/pulp/pulp_file/issues/605)
-   The relative_path field of PULP_MANIFEST can now contain commas, since they are valid filename characters in both Linux and Windows filesystems.
    [#630](https://github.com/pulp/pulp_file/issues/630)
-   Fixed a bug where publish used /tmp/ instead of the worker working directory.
    [#676](https://github.com/pulp/pulp_file/issues/676)

### Misc

-   [#691](https://github.com/pulp/pulp_file/issues/691)

---

## 1.10.5 (2022-08-16) {: #1.10.5 }

No significant changes.

---

## 1.10.4 (2022-08-15) {: #1.10.4 }

No significant changes.

---

## 1.10.3 (2022-06-22) {: #1.10.3 }

No significant changes.

---

## 1.10.2 (2022-02-23) {: #1.10.2 }

### Bugfixes

-   Fixed packaging bug which didn't allow pulp_file 1.10 to be installed with pulpcore 3.18.0.
    [#645](https://pulp.plan.io/issues/645)

---

## 1.10.1 (2021-11-02) {: #1.10.1 }

No significant changes.

---

## YANKED 1.10.0 (2021-10-06) {: #1.10.0 }

Yank reason: incompatible with dependencies, use 1.10.1 instead

### Features

-   Added in validation of ACS paths.
    [#9341](https://pulp.plan.io/issues/9341)
-   Added refresh endpoint for Alternate Content Sources.
    [#9377](https://pulp.plan.io/issues/9377)
-   Enabled remote type validation for the ACS.
    [#9384](https://pulp.plan.io/issues/9384)

### Bugfixes

-   Fixed bug where sync tasks would open a lot of DB connections.
    [#9252](https://pulp.plan.io/issues/9252)
-   Fixed bug where user hidden repos were visible to the user.
    [#9416](https://pulp.plan.io/issues/9416)
-   Check whether ACS exists before refreshing it.
    [#9420](https://pulp.plan.io/issues/9420)

### Improved Documentation

-   Updated ACS docs to use CLI.
    [#9373](https://pulp.plan.io/issues/9373)

### Misc

-   [#9357](https://pulp.plan.io/issues/9357), [#9426](https://pulp.plan.io/issues/9426)

---

## 1.9.1 (2021-08-30) {: #1.9.1 }

### Bugfixes

-   Fixed bug where sync tasks would open a lot of DB connections.
    (backported from #9252)
    [#9311](https://pulp.plan.io/issues/9311)

---

## 1.9.0 (2021-08-26) {: #1.9.0 }

### Features

-   Enable reclaim disk feature provided by pulpcore. This feature is available with pulpcore 3.15+.
    [#9168](https://pulp.plan.io/issues/9168)

### Bugfixes

-   Fix an issue where "mirror=True" syncs of a repository which has already been synced, and has not changed since the last sync, would fail.
    [#8999](https://pulp.plan.io/issues/8999)
-   Fixed failing 0012_delete_filefilesystemexporter migration which errors if there are
    `FileFilesystemExporters`.
    [#9102](https://pulp.plan.io/issues/9102)
-   Fixed filtering content by sha256 for on-demand content.
    [#9117](https://pulp.plan.io/issues/9117)

### Deprecations and Removals

-   Dropped support for Python 3.6 and 3.7. pulp_file now supports Python 3.8+.
    [#9037](https://pulp.plan.io/issues/9037)

### Misc

-   [#8959](https://pulp.plan.io/issues/8959), [#9154](https://pulp.plan.io/issues/9154)

---

## 1.8.2 (2021-07-21) {: #1.8.2 }

### Bugfixes

-   Fix an issue where "mirror=True" syncs of a repository which has already been synced, and has not changed since the last sync, would fail.
    (backported from #8999)
    [#9060](https://pulp.plan.io/issues/9060)
-   Fixed failing 0012_delete_filefilesystemexporter migration which errors if there are
    `FileFilesystemExporters`.
    (backported from #9102)
    [#9122](https://pulp.plan.io/issues/9122)

---

## 1.8.1 (2021-07-01) {: #1.8.1 }

### Misc

-   [#8969](https://pulp.plan.io/issues/8969)

---

## 1.8.0 (2021-06-11) {: #1.8.0 }

### Features

-   Auto-publish no longer modifies distributions.
    Auto-distribute now only requires setting a distribution's `repository` field.
    [#8762](https://pulp.plan.io/issues/8762)
-   Performing a sync with "mirror=True" will automatically generate a publication at sync-time.
    [#8851](https://pulp.plan.io/issues/8851)

### Deprecations and Removals

-   The filesystem export functionality has been removed from pulp_file. Users should now use the
    filesystem export functionaliy in pulpcore instead. Upgrading to pulp_file 1.8.0 will drop any
    `FilesystemExporters` in pulp_file.
    [#8861](https://pulp.plan.io/issues/8861)

### Misc

-   [#8719](https://pulp.plan.io/issues/8719)

---

## 1.7.0 (2021-04-16) {: #1.7.0 }

### Features

-   Add support for automatic publishing and distributing.
    [#7469](https://pulp.plan.io/issues/7469)

### Improved Documentation

-   Documented the auto-publication and auto-distribution feature.
    [#8548](https://pulp.plan.io/issues/8548)

### Misc

-   [#8387](https://pulp.plan.io/issues/8387), [#8415](https://pulp.plan.io/issues/8415), [#8508](https://pulp.plan.io/issues/8508)

---

## 1.6.1 (2021-03-30) {: #1.6.1 }

### Bugfixes

-   Added asynchronous tasking to the Update and Delete endpoints of FilesystemExporter to provide proper locking on resources.
    [#8451](https://pulp.plan.io/issues/8451)

### Deprecations and Removals

-   Update and Delete endpoints of FilesystemExporter changed to return 202 with tasks.
    [#8451](https://pulp.plan.io/issues/8451)

---

## 1.6.0 (2021-03-05) {: #1.6.0 }

### Bugfixes

-   Fixed a bug which caused the plugin to report the default manifest's name instead of the specified
    one in the publication endpoint.
    [#7838](https://pulp.plan.io/issues/7838)

### Improved Documentation

-   Update workflow docs to pulp-cli.
    [#7530](https://pulp.plan.io/issues/7530)
-   Add demo requirement to the Contributing process.
    [#7704](https://pulp.plan.io/issues/7704)
-   Update docs link in README.
    [#7932](https://pulp.plan.io/issues/7932)
-   Use the ReadTheDocs theme for pulp_file docs.
    [#8165](https://pulp.plan.io/issues/8165)

---

## 1.5.0 (2020-12-15) {: #1.5.0 }

No significant changes. Addressed pulpcore 3.9 deprecations.

---

## 1.4.0 (2020-12-02) {: #1.4.0 }

### Bugfixes

-   Added some missing files to MANIFEST.in.
    [#7685](https://pulp.plan.io/issues/7685)

### Improved Documentation

-   Documented that a functional test is now a requirement for a feature or a bug fix.
    [#7437](https://pulp.plan.io/issues/7437)

---

## 1.3.0 (2020-09-23) {: #1.3.0 }

### Bugfixes

-   Fixed exception when hitting `/pulp/api/v3/exporters/file/filesystem/<uuid>/exports/`.
    [#7522](https://pulp.plan.io/issues/7522)

### Improved Documentation

-   Added docs for using FileSystemExporter.
    [#7515](https://pulp.plan.io/issues/7515)

### Misc

-   [#7454](https://pulp.plan.io/issues/7454)

---

## 1.2.0 (2020-08-13) {: #1.2.0 }

### Features

-   Added ability for users to add Remote to Repository and automatically use it when syncing.
    [#7135](https://pulp.plan.io/issues/7135)

### Improved Documentation

-   Fixed the name of the artifact field
    [#5966](https://pulp.plan.io/issues/5966)

### Misc

-   [#6936](https://pulp.plan.io/issues/6936)

---

## 1.1.0 (2020-07-08) {: #1.1.0 }

### Bugfixes

-   Including requirements.txt on MANIFEST.in
    [#6885](https://pulp.plan.io/issues/6885)

### Improved Documentation

-   Added a remainder about the recommended utilities used in the workflows.
    [#5998](https://pulp.plan.io/issues/5998)
-   Updated fixture links from fedorapeople.org to fixtures.pulpproject.org.
    [#6653](https://pulp.plan.io/issues/6653)

---

## 1.0.1 (2020-06-03) {: #1.0.1 }

### Bugfixes

-   Including requirements.txt on MANIFEST.in
    [#6885](https://pulp.plan.io/issues/6885)

---

## 1.0.0 (2020-05-27) {: #1.0.0 }

### Misc

-   [#6514](https://pulp.plan.io/issues/6514), [#6708](https://pulp.plan.io/issues/6708), [#6730](https://pulp.plan.io/issues/6730), [#6761](https://pulp.plan.io/issues/6761)

---

## 0.3.0 (2020-04-16) {: #0.3.0 }

### Features

-   Added history for filesystem exports at `/exporters/file/filesystem/<uuid>/exports/`.
    [#6328](https://pulp.plan.io/issues/6328)
-   Add support for import/export processing
    [#6472](https://pulp.plan.io/issues/6472)

### Deprecations and Removals

-   The fileystem exporter endpoint has been moved from `/exporters/file/file/` to
    `/exporters/file/filesystem/` and the export endpoint is now at POST
    `/exporters/file/filesystem/<uuid>/exports/`. Additionally, the table is being dropped and
    recreated due to a data structure change in core so users will lose any filesystem exporter data on
    upgrade.
    [#6328](https://pulp.plan.io/issues/6328)

### Misc

-   [#6155](https://pulp.plan.io/issues/6155), [#6300](https://pulp.plan.io/issues/6300), [#6362](https://pulp.plan.io/issues/6362), [#6392](https://pulp.plan.io/issues/6392)

---

## 0.2.0 (2020-02-26) {: #0.2.0 }

### Deprecations and Removals

-   Renamed the filter for the field 'digest' to 'sha256' to correspond to field name in API and other
    plugins.
    [#5965](https://pulp.plan.io/issues/5965)

### Misc

-   [#5567](https://pulp.plan.io/issues/5567)

---

## 0.1.1 (2020-01-31) {: #0.1.1 }

### Bugfixes

-   Adjusts setup.py classifier to show 0.1.0 as Production/Stable.
    [#5897](https://pulp.plan.io/issues/5897)

### Misc

-   [#5867](https://pulp.plan.io/issues/5867), [#5872](https://pulp.plan.io/issues/5872), [#5967](https://pulp.plan.io/issues/5967), [#6016](https://pulp.plan.io/issues/6016)

---

## 0.1.0 (2019-12-12) {: #0.1.0 }

### Improved Documentation

-   Labeling Exporters as tech preview.
    [#5563](https://pulp.plan.io/issues/5563)

### Misc

-   [#5701](https://pulp.plan.io/issues/5701)

---

## 0.1.0rc2 (2019-12-03)

### Features

-   Add checking for path overlapping for RepositoryVersions and Publications.
    [#5559](https://pulp.plan.io/issues/5559)

### Misc

-   [#5757](https://pulp.plan.io/issues/5757)

---

## 0.1.0rc1 (2019-11-14)

### Features

-   Sync, Upload, and Modify now have added content with the same relative_path as existing content
    will remove the existing content.
    [#3541](https://pulp.plan.io/issues/3541)
-   Change relative_path from CharField to TextField
    [#4544](https://pulp.plan.io/issues/4544)
-   Added support for exporting file publications to the filesystem.
    [#5086](https://pulp.plan.io/issues/5086)

### Deprecations and Removals

-   Sync is no longer available at the {remote_href}/sync/ repository={repo_href} endpoint. Instead, use POST {repo_href}/sync/ remote={remote_href}.

    Creating / listing / editing / deleting file repositories is now performed on /pulp/api/v3/file/file/ instead of /pulp/api/v3/repositories/. Only file content can be present in a file repository, and only a file repository can hold file content.
    [#5625](https://pulp.plan.io/issues/5625)

### Misc

-   [#3308](https://pulp.plan.io/issues/3308), [#5458](https://pulp.plan.io/issues/5458), [#5580](https://pulp.plan.io/issues/5580), [#5629](https://pulp.plan.io/issues/5629)

---

## 0.1.0b4 (2019-10-15)

### Bugfixes

-   New RepositoryVersions will remove an existing unit at the same relative_path. This is true for
    both sync and upload, and is per Repository.
    [#4028](https://pulp.plan.io/issues/4028)

### Improved Documentation

-   Change the prefix of Pulp services from pulp-* to pulpcore-*
    [#4554](https://pulp.plan.io/issues/4554)

### Deprecations and Removals

-   Change _id, _created, _last_updated, _href to pulp_id, pulp_created, pulp_last_updated, pulp_href
    [#5457](https://pulp.plan.io/issues/5457)
-   Remove "_" from _versions_href, _latest_version_href
    [#5548](https://pulp.plan.io/issues/5548)
-   Removing base field: _type .
    [#5550](https://pulp.plan.io/issues/5550)

---

## 0.1.0b3 (2019-09-30)

### Features

-   Setting code on ProgressBar.
    [#5184](https://pulp.plan.io/issues/5184)
-   Add upload functionality to the file content endpoint.
    [#5403](https://pulp.plan.io/issues/5403)

### Deprecations and Removals

-   Adjust FileContentSerializer to upstream change.
    [#5428](https://pulp.plan.io/issues/5428)

### Misc

-   [#5304](https://pulp.plan.io/issues/5304), [#5444](https://pulp.plan.io/issues/5444)

---

## 0.1.0b2 (2019-09-11)

### Improved Documentation

-   Fix the code snippet provided in the example for creating a file content
    [#5094](https://pulp.plan.io/issues/5094)

### Misc

-   [#4681](https://pulp.plan.io/issues/4681)

---

## 0.1.0b1 (2019-07-09)

### Features

-   Override the Remote's serializer to allow policy='on_demand' and policy='streamed'.
    [#4990](https://pulp.plan.io/issues/4990)

### Improved Documentation

-   Switch to using [towncrier](https://github.com/hawkowl/towncrier) for better release notes.
    [#4875](https://pulp.plan.io/issues/4875)
