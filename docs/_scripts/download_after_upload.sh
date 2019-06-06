#!/usr/bin/env sh

# The distribution will return a url that can be used by http clients
echo "Setting DISTRIBUTION_BASE_URL, which is used to retrieve content from the content app."
export DISTRIBUTION_BASE_URL=$(http $BASE_ADDR$DISTRIBUTION_HREF | jq -r '.base_url')

echo "Downloading file from Distribution via the content app."
http -d http://$DISTRIBUTION_BASE_URL/$ARTIFACT_RELATIVE_PATH
