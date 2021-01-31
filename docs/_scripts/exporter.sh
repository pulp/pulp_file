#!/usr/bin/env bash

# TODO: convert file to pulp-cli once the filesystem exporter commands are implemented

export EXPORTER_NAME=$(head /dev/urandom | tr -dc a-z | head -c5)
export DEST_DIR=$(mktemp -d -t export-XXXXXXXX)

echo "Created a new file system exporter $EXPORTER_NAME."
export EXPORTER_HREF=$(http POST $BASE_ADDR/pulp/api/v3/exporters/file/filesystem/ \
  name=$EXPORTER_NAME path=$DEST_DIR | jq -r '.pulp_href')
