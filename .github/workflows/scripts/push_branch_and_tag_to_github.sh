#!/bin/sh

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_file' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -eu

BRANCH_NAME="$(echo "$GITHUB_REF" | sed -rn 's/refs\/heads\/(.*)/\1/p')"

remote_repo="https://pulpbot:${RELEASE_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

git push "${remote_repo}" "$BRANCH_NAME" "$1"
