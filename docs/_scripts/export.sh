#!/usr/bin/env bash

# TODO: convert file to pulp-cli once the filesystem exporter commands are implemented

export TASK_URL=$(http POST $BASE_ADDR$EXPORTER_HREF'exports/' publication=$PUBLICATION_HREF \
  | jq -r '.task')

pulp task show --wait --href $TASK_URL

echo "Inspecting export at $DEST_DIR"
ls $DEST_DIR
