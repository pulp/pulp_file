# Set environment variables for default hostname and ports for the API and the Content app
export BASE_ADDR=http://localhost:24817
export CONTENT_ADDR=http://localhost:24816

# Necessary for `django-admin`
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings

# Poll a Pulp task until it is finished.
wait_until_task_finished() {
    local task_url=$1
    while true
    do
        local response=$(http $task_url)
        local state=$(jq -r .state <<< ${response})
        jq . <<< "${response}"
        case ${state} in
            failed|completed|canceled)
                break
                ;;
            *)
                sleep 1
                ;;
        esac
    done
}
