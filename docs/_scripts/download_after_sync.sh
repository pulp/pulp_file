#!/usr/bin/env bash

# The distribution will return a url that can be used by http clients
echo "Setting DISTRIBUTION_BASE_URL, which is used to retrieve content from the content app."
export DISTRIBUTION_BASE_URL=$(http $BASE_ADDR$DISTRIBUTION_HREF | jq -r '.base_url')
# If Pulp was installed without CONTENT_HOST set, it's just the path.
# And httpie will default to localhost:80
if [[ "${DISTRIBUTION_BASE_URL:0:1}" = "/" ]]; then
    DISTRIBUTION_BASE_URL=$CONTENT_ADDR$DISTRIBUTION_BASE_URL
fi

# Next we download a file from the distribution
# This will default to http://
http -d $DISTRIBUTION_BASE_URL/test.iso
