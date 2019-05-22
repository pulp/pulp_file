# Create a new publication specifying the repository_version.
# Alternatively, you can specify the repository, and Pulp will assume the latest version.
export TASK_URL=$(http POST $BASE_ADDR/pulp/api/v3/publications/file/file/ \
  repository_version=$REPOVERSION_HREF | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

# After the task is complete, it gives us a new file publication
export PUBLICATION_HREF=$(http $BASE_ADDR$TASK_URL| jq -r '.created_resources | first')

# Lets inspect our newly created Publication.
http $BASE_ADDR$PUBLICATION_HREF
