#!/usr/bin/env bash
# coding=utf-8

set -mveuo pipefail

pytest -v -r sx --color=yes --pyargs pulp_file.tests.functional || show_logs_and_return_non_zero

PULPCORE_VERSION=$(http http://pulp/pulp/api/v3/status/ | jq -r '.versions'[0].version)

if [ "${GITHUB_REF##refs/tags/}" != "${GITHUB_REF}" ]
then
  cd ../pulpcore
  git fetch origin refs/tags/${PULPCORE_VERSION}
  git checkout FETCH_HEAD
  cd ../pulp_file
fi

if [ ${PULPCORE_VERSION::3} == "3.9" ]
then
  # Temporarily need to downgrade pulp-smash to run pulpcore 3.9 tests
  pip install 'pulp-smash==1!0.12.0'
fi

pytest -v -r sx --color=yes --pyargs pulpcore.tests.functional || show_logs_and_return_non_zero
