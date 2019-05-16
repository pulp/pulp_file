# Distributions are created asynchronously. Create one, and specify the publication that will
# be served at the base path specified.
export TASK_URL=$(http POST $BASE_ADDR/pulp/api/v3/distributions/file/file/ \
  name='baz' \
  base_path='foo' \
  publication=$PUBLICATION_HREF | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

# After the task is complete, it gives us a new file distribution
export DISTRIBUTION_HREF=$(http $BASE_ADDR$TASK_URL| jq -r '.created_resources | first')

# Lets inspect the Distribution
http $BASE_ADDR$DISTRIBUTION_HREF
