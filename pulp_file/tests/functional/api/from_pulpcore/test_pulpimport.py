"""
Tests PulpImporter and PulpImport functionality

NOTE: assumes ALLOWED_EXPORT_PATHS and ALLOWED_IMPORT_PATHS settings contain "/tmp" - all tests
will fail if this is not the case.
"""
import json
import subprocess
import pytest
import uuid

from pulpcore.tests.functional.utils import monitor_task, monitor_task_group

from pulpcore.app import settings

from pulpcore.client.pulpcore.exceptions import ApiException

from pulpcore.client.pulp_file import RepositorySyncURL

NUM_REPOS = 2


if "/tmp" not in settings.ALLOWED_IMPORT_PATHS:
    raise pytest.skip(
        "Cannot run import-tests unless /tmp is in ALLOWED_IMPORT_PATHS ({}).".format(
            settings.ALLOWED_IMPORT_PATHS
        ),
        allow_module_level=True,
    )


@pytest.fixture
def import_export_repositories(
    file_repo_api_client,
    file_fixture_gen_file_repo,
    file_fixture_gen_remote_ssl,
    basic_manifest_path,
):
    import_repos = []
    export_repos = []
    for r in range(NUM_REPOS):
        import_repo = file_fixture_gen_file_repo()
        export_repo = file_fixture_gen_file_repo()

        remote = file_fixture_gen_remote_ssl(manifest_path=basic_manifest_path, policy="immediate")
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = file_repo_api_client.sync(export_repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)

        export_repo = file_repo_api_client.read(export_repo.pulp_href)

        export_repos.append(export_repo)
        import_repos.append(import_repo)

    return import_repos, export_repos


@pytest.fixture
def created_exporter(
    gen_object_with_cleanup, exporters_pulp_api_client, import_export_repositories
):
    _, export_repos = import_export_repositories
    body = {
        "name": str(uuid.uuid4()),
        "repositories": [r.pulp_href for r in export_repos],
        "path": "/tmp/{}".format(str(uuid.uuid4())),
    }
    exporter = gen_object_with_cleanup(exporters_pulp_api_client, body)
    return exporter


@pytest.fixture
def created_export(exporters_pulp_exports_api_client, created_exporter):
    export_response = exporters_pulp_exports_api_client.create(created_exporter.pulp_href, {})
    export_href = monitor_task(export_response.task).created_resources[0]
    export = exporters_pulp_exports_api_client.read(export_href)
    return export


@pytest.fixture
def chunked_export(exporters_pulp_exports_api_client, created_exporter):
    export_response = exporters_pulp_exports_api_client.create(
        created_exporter.pulp_href, {"chunk_size": "5KB"}
    )
    export_href = monitor_task(export_response.task).created_resources[0]
    export = exporters_pulp_exports_api_client.read(export_href)
    return export


@pytest.fixture
def import_check_directory():
    """Creates a directory/file structure for testing import-check"""
    tmpdir = f"/tmp/importcheck/{uuid.uuid4()}"

    subprocess.check_output(
        f"mkdir -p {tmpdir}/noreaddir {tmpdir}/nowritedir {tmpdir}/nowritedir/notafile",
        shell=True,
    )

    subprocess.check_output(f"touch {tmpdir}/noreadfile", shell=True)
    subprocess.check_output(f"touch {tmpdir}/noreaddir/goodfile", shell=True)
    subprocess.check_output(f"touch {tmpdir}/nowritedir/goodfile", shell=True)
    subprocess.check_output(f"touch {tmpdir}/nowritedir/noreadfile", shell=True)

    subprocess.check_output(f"chmod 333 {tmpdir}/nowritedir/noreadfile", shell=True)
    subprocess.check_output(f"chmod 333 {tmpdir}/noreadfile", shell=True)
    subprocess.check_output(f"chmod 333 {tmpdir}/noreaddir", shell=True)
    subprocess.check_output(f"chmod 555 {tmpdir}/nowritedir", shell=True)

    yield tmpdir

    subprocess.check_output(f"chmod -R +rwx {tmpdir}/", shell=True)
    subprocess.check_output(f"rm -rf {tmpdir}", shell=True)


@pytest.fixture
def pulp_importer_factory(
    gen_object_with_cleanup, import_export_repositories, importers_pulp_api_client
):
    def _pulp_importer_factory(name=None, exported_repos=None):
        """Create an importer."""
        _import_repos, _exported_repos = import_export_repositories
        mapping = {}
        if not name:
            name = str(uuid.uuid4())
        if not exported_repos:
            exported_repos = _exported_repos

        for idx, repo in enumerate(exported_repos):
            mapping[repo.name] = _import_repos[idx].name

        body = {
            "name": name,
            "repo_mapping": mapping,
        }

        importer = gen_object_with_cleanup(importers_pulp_api_client, body)

        return importer

    return _pulp_importer_factory


def _find_toc(chunked_export):
    filenames = [f for f in list(chunked_export.output_file_info.keys()) if f.endswith("json")]
    return filenames[0]


def _find_path(created_export):
    filenames = [f for f in list(created_export.output_file_info.keys()) if f.endswith("tar.gz")]
    return filenames[0]


@pytest.fixture
def perform_import(chunked_export, created_export, importers_pulp_imports_api_client):
    def _perform_import(importer, chunked=False, an_export=None):
        """Perform an import with importer."""
        if not an_export:
            an_export = chunked_export if chunked else created_export

        if chunked:
            filenames = [f for f in list(an_export.output_file_info.keys()) if f.endswith("json")]
            import_response = importers_pulp_imports_api_client.create(
                importer.pulp_href, {"toc": filenames[0]}
            )
        else:
            filenames = [f for f in list(an_export.output_file_info.keys()) if f.endswith("tar.gz")]
            import_response = importers_pulp_imports_api_client.create(
                importer.pulp_href, {"path": filenames[0]}
            )
        task_group = monitor_task_group(import_response.task_group)

        return task_group

    return _perform_import


def test_importer_create(pulp_importer_factory, importers_pulp_api_client):
    """Test creating an importer."""
    name = str(uuid.uuid4())
    importer = pulp_importer_factory(name)
    assert importer.name == name

    importer = importers_pulp_api_client.read(importer.pulp_href)
    assert importer.name == name


def test_importer_delete(pulp_importer_factory, importers_pulp_api_client):
    """Test deleting an importer."""
    importer = pulp_importer_factory()

    importers_pulp_api_client.delete(importer.pulp_href)

    with pytest.raises(ApiException) as ae:
        importers_pulp_api_client.read(importer.pulp_href)
    assert 404 == ae.value.status


def test_import(
    pulp_importer_factory, file_repo_api_client, import_export_repositories, perform_import
):
    """Test an import."""
    import_repos, exported_repos = import_export_repositories
    importer = pulp_importer_factory()
    task_group = perform_import(importer)
    assert (len(import_repos) + 1) == task_group.completed

    for report in task_group.group_progress_reports:
        if report.code == "import.repo.versions":
            assert report.done == len(import_repos)

    for repo in import_repos:
        repo = file_repo_api_client.read(repo.pulp_href)
        assert f"{repo.pulp_href}versions/1/" == repo.latest_version_href


@pytest.mark.parallel
def test_double_import(
    pulp_importer_factory,
    importers_pulp_imports_api_client,
    import_export_repositories,
    file_repo_api_client,
    perform_import,
):
    """Test two imports of our export."""
    import_repos, exported_repos = import_export_repositories

    importer = pulp_importer_factory()
    perform_import(importer)
    perform_import(importer)

    imports = importers_pulp_imports_api_client.list(importer.pulp_href).results
    assert len(imports) == 2

    for repo in import_repos:
        repo = file_repo_api_client.read(repo.pulp_href)
        # still only one version as pulp won't create a new version if nothing changed
        assert f"{repo.pulp_href}versions/1/" == repo.latest_version_href


@pytest.mark.parallel
def test_chunked_import(
    pulp_importer_factory, import_export_repositories, file_repo_api_client, perform_import
):
    """Test an import."""
    import_repos, exported_repos = import_export_repositories
    importer = pulp_importer_factory()
    task_group = perform_import(importer, chunked=True)
    assert (len(import_repos) + 1) == task_group.completed

    for repo in import_repos:
        repo = file_repo_api_client.read(repo.pulp_href)
        assert f"{repo.pulp_href}versions/1/" == repo.latest_version_href


@pytest.mark.parallel
def test_import_check_valid_path(created_export, importers_pulp_imports_check_api_client):
    body = {"path": _find_path(created_export)}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.path.context == _find_path(created_export)
    assert result.path.is_valid
    assert len(result.path.messages) == 0
    assert result.toc is None
    assert result.repo_mapping is None


@pytest.mark.parallel
def test_import_check_valid_toc(chunked_export, importers_pulp_imports_check_api_client):
    body = {"toc": _find_toc(chunked_export)}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.toc.context == _find_toc(chunked_export)
    assert result.toc.is_valid
    assert len(result.toc.messages) == 0
    assert result.path is None
    assert result.repo_mapping is None


@pytest.mark.parallel
def test_import_check_repo_mapping(importers_pulp_imports_check_api_client):
    body = {"repo_mapping": json.dumps({"foo": "bar"})}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.repo_mapping.context == json.dumps({"foo": "bar"})
    assert result.repo_mapping.is_valid
    assert len(result.repo_mapping.messages) == 0
    assert result.path is None
    assert result.toc is None

    body = {"repo_mapping": '{"foo": "bar"'}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.repo_mapping.context == '{"foo": "bar"'
    assert not result.repo_mapping.is_valid
    assert result.repo_mapping.messages[0] == "invalid JSON"


@pytest.mark.parallel
def test_import_check_not_allowed(importers_pulp_imports_check_api_client):
    body = {"path": "/notinallowedimports"}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.path.context == "/notinallowedimports"
    assert not result.path.is_valid
    assert len(result.path.messages) == 1, "Only not-allowed should be returned"
    assert result.path.messages[0] == "/ is not an allowed import path"

    body = {"toc": "/notinallowedimports"}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.toc.context == "/notinallowedimports"
    assert not result.toc.is_valid
    assert len(result.toc.messages) == 1, "Only not-allowed should be returned"
    assert result.toc.messages[0] == "/ is not an allowed import path"


@pytest.mark.parallel
def test_import_check_no_file(importers_pulp_imports_check_api_client):
    body = {"path": "/tmp/idonotexist"}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.path.context == "/tmp/idonotexist"
    assert not result.path.is_valid
    assert any("file /tmp/idonotexist does not exist" in s for s in result.path.messages)

    body = {"toc": "/tmp/idonotexist"}
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.toc.context == "/tmp/idonotexist"
    assert not result.toc.is_valid
    assert any("file /tmp/idonotexist does not exist" in s for s in result.toc.messages)


@pytest.mark.parallel
def test_import_check_all_valid(
    created_export, chunked_export, importers_pulp_imports_check_api_client
):
    body = {
        "path": _find_path(created_export),
        "toc": _find_toc(chunked_export),
        "repo_mapping": json.dumps({"foo": "bar"}),
    }
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)
    assert result.path.context == _find_path(created_export)
    assert result.toc.context == _find_toc(chunked_export)
    assert result.repo_mapping.context == json.dumps({"foo": "bar"})

    assert result.path.is_valid
    assert result.toc.is_valid
    assert result.repo_mapping.is_valid

    assert len(result.path.messages) == 0
    assert len(result.toc.messages) == 0
    assert len(result.repo_mapping.messages) == 0


@pytest.mark.parallel
def test_import_check_multiple_errors(
    importers_pulp_imports_check_api_client, import_check_directory
):
    body = {
        "path": "/notinallowedimports",
        "toc": f"{import_check_directory}/nowritedir/notafile",
        "repo_mapping": '{"foo": "bar"',
    }
    result = importers_pulp_imports_check_api_client.pulp_import_check_post(body)

    assert not result.path.is_valid
    assert len(result.path.messages) == 1, "Only not-allowed should be returned"
    assert result.path.messages[0] == "/ is not an allowed import path"

    assert not result.toc.is_valid
    assert any(
        f"{import_check_directory}/nowritedir/notafile is not a file" in s
        for s in result.toc.messages
    )
    assert any(
        f"directory {import_check_directory}/nowritedir must allow pulp write-access" in s
        for s in result.toc.messages
    )

    assert not result.repo_mapping.is_valid
    assert result.repo_mapping.messages[0] == "invalid JSON"


@pytest.fixture
def generate_export(exporters_pulp_exports_api_client):
    """Create and read back an export for the specified PulpExporter."""

    def _generate_export(exporter, body=None):
        if body is None:
            body = {}

        export_response = exporters_pulp_exports_api_client.create(exporter.pulp_href, body)
        export_href = monitor_task(export_response.task).created_resources[0]
        export = exporters_pulp_exports_api_client.read(export_href)

        return export

    return _generate_export


@pytest.fixture
def exported_version(
    pulp_importer_factory,
    gen_object_with_cleanup,
    import_export_repositories,
    exporters_pulp_api_client,
    exporters_pulp_exports_api_client,
    generate_export,
    perform_import,
    file_repo,
    file_repo_api_client,
    file_repo_ver_api_client,
    content_api_client,
    add_to_cleanup,
):
    import_repos, export_repos = import_export_repositories

    file_list = content_api_client.list(repository_version=export_repos[0].latest_version_href)

    # copy files from repositories[0] into new, one file at a time
    results = file_list.results
    for a_file in results:
        href = a_file.pulp_href
        modify_response = file_repo_api_client.modify(
            file_repo.pulp_href, {"add_content_units": [href]}
        )
        monitor_task(modify_response.task)
    # get all versions of that repo
    versions = file_repo_ver_api_client.list(file_repo.pulp_href, ordering=["number"])

    body = {
        "name": str(uuid.uuid4()),
        "repositories": [file_repo.pulp_href],
        "path": "/tmp/{}".format(str(uuid.uuid4())),
    }
    exporter = gen_object_with_cleanup(exporters_pulp_api_client, body)

    # export from version-0 to version-1, last=v1
    body = {
        "start_versions": [versions.results[0].pulp_href],
        "versions": [versions.results[1].pulp_href],
        "full": False,
    }
    export = generate_export(exporter, body)

    importer = pulp_importer_factory(exported_repos=[file_repo])
    task_group = perform_import(importer, chunked=False, an_export=export)

    return import_repos, task_group


@pytest.mark.parallel
def test_import_not_latest_version(exported_version, file_repo_api_client):
    """Test an import."""
    import_repos, task_group = exported_version
    for report in task_group.group_progress_reports:
        if report.code == "import.repo.versions":
            assert report.done == 1

    imported_repo = file_repo_api_client.read(import_repos[0].pulp_href)
    assert f"{imported_repo.pulp_href}versions/0/" != imported_repo.latest_version_href
