#!/usr/bin/env sh

export BASE_ADDR=https://pulp:443

cd docs/_scripts/
bash docs_check_upload_publish.sh
bash docs_check_sync_publish.sh
