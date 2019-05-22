# Manually add content to a repository by creating a new version, creating a task
export TASK_URL=$(http POST $BASE_ADDR$REPO_HREF'versions/' \
    add_content_units:="[\"$CONTENT_HREF\"]" \
    | jq -r '.task')

# Poll the task (here we use a function defined in docs/_scripts/base.sh)
wait_until_task_finished $BASE_ADDR$TASK_URL

# After the task is complete, it gives us a new repository version
export REPOVERSION_HREF=$(http $BASE_ADDR$TASK_URL| jq -r '.created_resources | first')

# Lets inspect our newly created RepositoryVersion
http $BASE_ADDR$REPOVERSION_HREF
