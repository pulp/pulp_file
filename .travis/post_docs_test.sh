#!/usr/bin/env sh

export BASE_ADDR=http://pulp:80
export CONTENT_ADDR=http://pulp:80

cd docs/_scripts/
bash docs_check_upload_publish.sh
bash docs_check_sync_publish.sh
