#!/usr/bin/env bash
echo "Creating a remote that points to an external source of files."
http POST $BASE_ADDR/pulp/api/v3/remotes/file/file/ \
    name='bar' \
    url='https://fixtures.pulpproject.org/file/PULP_MANIFEST'

echo "Export an environment variable for the new remote URI."
export REMOTE_HREF=$(http $BASE_ADDR/pulp/api/v3/remotes/file/file/ | jq -r '.results[] | select(.name == "bar") | .pulp_href')

echo "Inspecting new Remote."
http $BASE_ADDR$REMOTE_HREF
