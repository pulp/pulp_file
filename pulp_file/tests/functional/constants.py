# coding=utf-8
"""Constants for Pulp File plugin tests."""
from urllib.parse import urljoin

from pulp_smash.constants import PULP_FIXTURES_BASE_URL
from pulp_smash.pulp3.constants import (
    BASE_PUBLISHER_PATH,
    BASE_REMOTE_PATH,
    CONTENT_PATH
)

FILE_CONTENT_NAME = 'file.file'

FILE_CONTENT_PATH = urljoin(CONTENT_PATH, 'file/files/')

FILE_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, 'file/file/')

FILE_PUBLISHER_PATH = urljoin(BASE_PUBLISHER_PATH, 'file/file/')

FILE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'file/')
"""The URL to a file repository."""

FILE_FIXTURE_MANIFEST_URL = urljoin(FILE_FIXTURE_URL, 'PULP_MANIFEST')
"""The URL to a file repository manifest."""

FILE_FIXTURE_COUNT = 3
"""The number of packages available at :data:`FILE_FIXTURE_URL`."""

FILE_FIXTURE_SUMMARY = {
    FILE_CONTENT_NAME: {'count': FILE_FIXTURE_COUNT},
}
"""The desired content summary after syncing :data:`FILE_FIXTURE_URL`."""

FILE_URL = urljoin(FILE_FIXTURE_URL, '1.iso')
"""The URL to an ISO file at :data:`FILE_FIXTURE_URL`."""

FILE2_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'file2/')
"""The URL to a file repository."""

FILE2_FIXTURE_MANIFEST_URL = urljoin(FILE2_FIXTURE_URL, 'PULP_MANIFEST')
"""The URL to a file repository manifest"""

FILE2_URL = urljoin(FILE2_FIXTURE_URL, '1.iso')
"""The URL to an ISO file at :data:`FILE2_FIXTURE_URL`."""

FILE_INVALID_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'file-invalid/')
"""The URL to an invalid file repository."""

FILE_INVALID_MANIFEST_URL = urljoin(FILE_INVALID_FIXTURE_URL, 'PULP_MANIFEST')
"""The URL to an invalid file repository."""

FILE_LARGE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'file-large/')
"""The URL to a file repository containing a large number of files."""

FILE_LARGE_FIXTURE_MANIFEST_URL = urljoin(
    FILE_LARGE_FIXTURE_URL,
    'PULP_MANIFEST'
)
"""The URL to a file repository manifest."""
