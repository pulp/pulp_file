#!/usr/bin/env bash
DISTRIBUTION_BASE_URL=$(pulp file distribution show --name $DIST_NAME | jq -r '.base_url')

# Next we download a file from the distribution
echo "Downloading file from Distribution via the content app."
http -d $DISTRIBUTION_BASE_URL/1.iso
