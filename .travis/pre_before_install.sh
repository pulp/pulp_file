#!/usr/bin/env bash

set -mveuo pipefail

# skip this check for everything but PRs
if [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
  exit 0
fi

if [ "$TRAVIS_COMMIT_RANGE" != "" ]; then
  RANGE=$TRAVIS_COMMIT_RANGE
elif [ "$TRAVIS_COMMIT" != "" ]; then
  RANGE="$TRAVIS_COMMIT~...$TRAVIS_COMMIT"
fi


REQUIRES_TEST=$(git diff --name-only $RANGE | grep -E 'feature|bugfix')
CONTAINS_TEST=$(git diff --name-only $RANGE | grep -E '^test_')

if [ -n $REQUIRES_TEST ] && ![ -n $CONTAINS_TEST ]; then
  echo "Test required for feature/bugfix."
  exit 1
fi
