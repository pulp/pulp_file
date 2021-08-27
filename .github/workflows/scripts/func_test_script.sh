#!/usr/bin/env bash
# coding=utf-8

set -mveuo pipefail

pytest -v -r sx --color=yes --pyargs pulp_file.tests.functional

if [ "${GITHUB_REF##refs/tags/}" != "${GITHUB_REF}" ]
then
  PULPCORE_VERSION=$(http http://pulp/pulp/api/v3/status/ | jq -r '.versions'[0].version)
  cd ../pulpcore
  git fetch origin refs/tags/${PULPCORE_VERSION}
  git checkout FETCH_HEAD
  cd ../pulp_file
  if [ ${PULPCORE_VERSION::3} == "3.9" ]
  then
    # Temporarily need to downgrade pulp-smash to run pulpcore 3.9 tests
    pip install 'pulp-smash==1!0.12.0'
  fi
fi

pip install -r ../pulpcore/functest_requirements.txt

pytest -v -r sx --color=yes --pyargs pulpcore.tests.functional
