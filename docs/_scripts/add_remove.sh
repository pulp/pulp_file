#!/usr/bin/env bash

echo "Kick off a task to add content to a repository, storing TASK_URL env variable"
export TASK_URL=$(http POST $BASE_ADDR$REPO_HREF'versions/' \
    add_content_units:="[\"$CONTENT_HREF\"]" \
    | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

echo "Retrieving REPOVERSION_HREF from task"
export REPOVERSION_HREF=$(http $BASE_ADDR$TASK_URL| jq -r '.created_resources | first')

echo "Inspecting repository version."
http $BASE_ADDR$REPOVERSION_HREF
