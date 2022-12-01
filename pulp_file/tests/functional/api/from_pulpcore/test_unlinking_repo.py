"""Tests that perform action over remotes"""
import pytest
from pulp_smash.pulp3.utils import gen_repo


@pytest.mark.parallel
def test_shared_remote_usage(
    file_repo_api_client,
    file_content_api_client,
    file_fixture_gen_remote_ssl,
    basic_manifest_path,
    gen_object_with_cleanup,
    monitor_task,
):
    """Verify remotes can be used with different repos."""
    remote = file_fixture_gen_remote_ssl(manifest_path=basic_manifest_path, policy="on_demand")

    # Create and sync repos.
    repos = []
    for _ in range(2):
        repo = gen_object_with_cleanup(file_repo_api_client, gen_repo())
        monitor_task(file_repo_api_client.sync(repo.pulp_href, {"remote": remote.pulp_href}).task)
        repos.append(file_repo_api_client.read(repo.pulp_href))

    # Compare contents of repositories.
    contents = set()
    for repo in repos:
        content = file_content_api_client.list(repository_version=repo.latest_version_href)
        assert content.count == 3
        contents.update({c.pulp_href for c in content.results})
    assert len(contents) == 3
