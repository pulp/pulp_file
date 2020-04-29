#!/usr/bin/env bash

echo 'Create File Content from the artifact and save as environment variable'
export TASK_URL=$(http POST $BASE_ADDR/pulp/api/v3/content/file/files/ \
    relative_path="test_upload.txt" \
    artifact=$ARTIFACT_HREF \
    | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

# After the task is complete, it gives us a new content
echo "Set CONTENT_HREF from finished task."
export CONTENT_HREF=$(http $BASE_ADDR$TASK_URL| jq -r '.created_resources | first')

echo "Inspecting new file content"
http $BASE_ADDR$CONTENT_HREF
