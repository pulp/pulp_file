#!/usr/bin/env bash
export REMOTE_NAME=$(head /dev/urandom | tr -dc a-z | head -c5)
echo "Creating a remote that points to an external source of files."
pulp file remote create --name $REMOTE_NAME \
    --url 'https://fixtures.pulpproject.org/file/PULP_MANIFEST'

echo "Inspecting new Remote."
pulp file remote show --name $REMOTE_NAME
