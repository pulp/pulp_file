#!/usr/bin/env bash
# coding=utf-8

set -mveuo pipefail

export POST_SCRIPT=$TRAVIS_BUILD_DIR/.travis/post_script.sh
export POST_DOCS_TEST=$TRAVIS_BUILD_DIR/.travis/post_docs_test.sh

# Needed for both starting the service and building the docs.
# Gets set in .travis/settings.yml, but doesn't seem to inherited by
# this script.
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings

wait_for_pulp() {
  TIMEOUT=${1:-5}
  while [ "$TIMEOUT" -gt 0 ]
  do
    echo -n .
    sleep 1
    TIMEOUT=$(($TIMEOUT - 1))
    if [ $(http :24817/pulp/api/v3/status/ | jq '.database_connection.connected and .redis_connection.connected') = 'true' ]
    then
      echo
      return
    fi
  done
  echo
  return 1
}

if [ "$TEST" = 'docs' ]; then
  sleep 5
  cd docs
  make html
  cd ..

  if [ -x $POST_DOCS_TEST ]; then
      $POST_DOCS_TEST
  fi
  exit
fi

if [ "$TEST" = 'bindings' ]; then
  COMMIT_MSG=$(git log --format=%B --no-merges -1)
  export PULP_BINDINGS_PR_NUMBER=$(echo $COMMIT_MSG | grep -oP 'Required\ PR:\ https\:\/\/github\.com\/pulp\/pulp-openapi-generator\/pull\/(\d+)' | awk -F'/' '{print $7}')

  cd ..
  git clone https://github.com/pulp/pulp-openapi-generator.git
  cd pulp-openapi-generator

  if [ -n "$PULP_BINDINGS_PR_NUMBER" ]; then
    git fetch origin +refs/pull/$PULP_BINDINGS_PR_NUMBER/merge
    git checkout FETCH_HEAD
  fi

  ./generate.sh pulpcore python
  pip install ./pulpcore-client
  ./generate.sh pulp_file python
  pip install ./pulp_file-client

  python $TRAVIS_BUILD_DIR/.travis/test_bindings.py
  exit
fi

# Run unit tests.
coverage run $(which django-admin) test ./pulp_file/tests/unit/

# Run functional tests, and upload coverage report to codecov.
show_logs_and_return_non_zero() {
    readonly local rc="$?"
    cat ~/django_runserver.log
    cat ~/content_app.log
    cat ~/resource_manager.log
    cat ~/reserved_worker-1.log
    return "${rc}"
}

# Stop services started by ansible roles
sudo systemctl stop pulp-worker* pulp-resource-manager pulp-content-app pulp-api

# Start services with logs and coverage
export PULP_CONTENT_HOST=localhost:24816
rq worker -n 'resource-manager@%h' -w 'pulpcore.tasking.worker.PulpWorker' -c 'pulpcore.rqconfig' >> ~/resource_manager.log 2>&1 &
rq worker -n 'reserved-resource-worker-1@%h' -w 'pulpcore.tasking.worker.PulpWorker' -c 'pulpcore.rqconfig' >> ~/reserved_worker-1.log 2>&1 &
gunicorn pulpcore.tests.functional.content_with_coverage:server --bind 'localhost:24816' --worker-class 'aiohttp.GunicornWebWorker' -w 2 >> ~/content_app.log 2>&1 &
coverage run $(which django-admin) runserver 24817 --noreload >> ~/django_runserver.log 2>&1 &
wait_for_pulp 20

# Run functional tests
pytest -v -r sx --color=yes --pyargs pulpcore.tests.functional || show_logs_and_return_non_zero
pytest -v -r sx --color=yes --pyargs pulp_file.tests.functional || show_logs_and_return_non_zero



if [ -x $POST_SCRIPT ]; then
    $POST_SCRIPT
fi
