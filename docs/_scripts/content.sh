#!/usr/bin/env bash

echo 'Create File Content from the artifact and save as environment variable'
export CONTENT_HREF=$(http POST $BASE_ADDR/pulp/api/v3/content/file/files/ \
    relative_path="test_upload.txt" \
    _artifact=$ARTIFACT_HREF \
    | jq -r .'pulp_href')

echo "Inspecting new file content"
http $BASE_ADDR$CONTENT_HREF
