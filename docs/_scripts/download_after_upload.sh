#!/usr/bin/env bash
DISTRIBUTION_BASE_URL=$(pulp file distribution show --name $DIST_NAME | jq -r '.base_url')

echo "Downloading file from Distribution via the content app."
# This will default to http://
http -d $DISTRIBUTION_BASE_URL/$ARTIFACT_RELATIVE_PATH
