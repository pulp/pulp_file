echo "Creating a remote that points to an external source of files."
http POST http://localhost:24817/pulp/api/v3/remotes/file/file/ \
    name='bar' \
    url='https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST'

echo "Export an environment variable for the new remote URI."
export REMOTE_HREF=$(http $BASE_ADDR/pulp/api/v3/remotes/file/file/ | jq -r '.results[] | select(.name == "bar") | ._href')

echo "Inspecting new Remote."
http $BASE_ADDR$REMOTE_HREF
