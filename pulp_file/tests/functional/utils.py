# coding=utf-8
"""Utilities for tests for the file plugin."""
from functools import partial
from unittest import SkipTest
from urllib.parse import urljoin

from pulp_smash import api, selectors
from pulp_smash.pulp3.constants import (
    FILE_CONTENT_PATH,
    FILE_REMOTE_PATH,
    REPO_PATH,
)
from pulp_smash.pulp3.utils import (
    gen_remote,
    gen_repo,
    require_pulp_3,
    require_pulp_plugins,
    sync,
)

from pulp_file.tests.functional.constants import FILE_FIXTURE_URL


def populate_pulp(cfg, url=None):
    """Add file contents to Pulp.

    :param pulp_smash.config.PulpSmashConfig: Information about a Pulp
        application.
    :param url: The URL to a file repository's ``PULP_MANIFEST`` file. Defaults
        to :data:`pulp_smash.constants.FILE_FIXTURE_URL` + ``PULP_MANIFEST``.
    :returns: A list of dicts, where each dict describes one file content in
        Pulp.
    """
    if url is None:
        url = urljoin(FILE_FIXTURE_URL, 'PULP_MANIFEST')
    client = api.Client(cfg, api.json_handler)
    remote = {}
    repo = {}
    try:
        remote.update(client.post(FILE_REMOTE_PATH, gen_remote(url)))
        repo.update(client.post(REPO_PATH, gen_repo()))
        sync(cfg, remote, repo)
    finally:
        if remote:
            client.delete(remote['_href'])
        if repo:
            client.delete(repo['_href'])
    return client.get(FILE_CONTENT_PATH)['results']


def set_up_module():
    """Skip tests Pulp 3 isn't under test or if pulp-file isn't installed."""
    require_pulp_3(SkipTest)
    require_pulp_plugins({'pulp_file'}, SkipTest)


skip_if = partial(selectors.skip_if, exc=SkipTest)  # pylint:disable=invalid-name
"""The ``@skip_if`` decorator, customized for unittest.

:func:`pulp_smash.selectors.skip_if` is test runner agnostic. This function is
identical, except that ``exc`` has been set to ``unittest.SkipTest``.
"""
