#!/usr/bin/env bash
export EXPORTER_NAME=$(head /dev/urandom | tr -dc a-z | head -c5)
export DEST_DIR="/data"

echo "Created a new file system exporter $EXPORTER_NAME."
export EXPORTER_HREF=$(http POST $BASE_ADDR/pulp/api/v3/exporters/file/filesystem/ \
  name=$EXPORTER_NAME path=$DEST_DIR | jq -r '.pulp_href')

export TASK_URL=$(http POST $BASE_ADDR$EXPORTER_HREF'exports/' publication=$PUBLICATION_HREF
  | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

echo "Inspecting export at $DEST_DIR"
ls $DEST_DIR
