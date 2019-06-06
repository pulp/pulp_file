#!/usr/bin/env sh

export DIST_NAME=$(head /dev/urandom | tr -dc a-z | head -c5)
export DIST_BASE_PATH=$(head /dev/urandom | tr -dc a-z | head -c5)

# Distributions are created asynchronously.
echo "Creating distribution \
  (name=$DIST_NAME, base_path=$DIST_BASE_PATH publication=$PUBLICATION_HREF)."
export TASK_URL=$(http POST $BASE_ADDR/pulp/api/v3/distributions/file/file/ \
  name=$DIST_NAME \
  base_path=$DIST_BASE_PATH \
  publication=$PUBLICATION_HREF | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

echo "Setting DISTRIBUTION_HREF from the completed task."
# DISTRIBUTION_HREF is the pulp-api HREF, not the content app href
export DISTRIBUTION_HREF=$(http $BASE_ADDR$TASK_URL| jq -r '.created_resources | first')

echo "Inspecting Distribution."
http $BASE_ADDR$DISTRIBUTION_HREF
