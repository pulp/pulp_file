# coding=utf-8
"""Tests that communicate with file plugin via the v3 API."""
from .test_acs import AlternateContentSourceTestCase

from .test_auto_publish import AutoPublishDistributeTestCase

from .test_crud_content_unit import (
    ContentUnitTestCase,
    ContentUnitUploadTestCase,
    DuplicateContentUnit,
    DuplicateRelativePathsInRepo,
)

from .test_crud_remotes import (
    CRUDRemotesTestCase,
    CreateRemoteNoURLTestCase,
    RemoteDownloadPolicyTestCase,
)

from .test_download_content import DownloadContentTestCase

from .test_download_policies import (
    SyncPublishDownloadPolicyTestCase,
    LazySyncedContentAccessTestCase,
    SwitchDownloadPolicyTestCase,
)

from .test_publish import PublishAnyRepoVersionTestCase

from .test_pulp_manifest import AccessingPublishedDataTestCase

from .test_sync import (
    BasicSyncTestCase,
    MirrorSyncTestCase,
    SyncInvalidTestCase,
    SyncDuplicateFileRepoTestCase,
)
