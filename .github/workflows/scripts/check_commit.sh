#!/bin/bash

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --travis pulp_file' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -euv

echo ::group::REQUESTS
pip3 install requests
echo ::endgroup::

# for sha in $(git rev-list $HEAD_COMMIT..)
for sha in $(curl $GITHUB_CONTEXT | jq '.[].sha' | sed 's/"//g')
do
  python3 .scripts/validate_commit_message.py $sha
  VALUE=$?
  if [ "$VALUE" -gt 0 ]; then
    exit $VALUE
  fi
done
