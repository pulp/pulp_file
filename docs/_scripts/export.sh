#!/usr/bin/env bash
export TASK_URL=$(http POST $BASE_ADDR$EXPORTER_HREF'exports/' publication=$PUBLICATION_HREF \
  | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

echo "Inspecting export at $DEST_DIR"
ls $DEST_DIR
