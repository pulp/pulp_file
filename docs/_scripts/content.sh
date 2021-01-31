#!/usr/bin/env bash

echo 'Create File Content from the artifact and save as environment variable'
CONTENT_HREF=$(pulp file content create --relative-path "test_upload.txt" --sha256 $ARTIFACT_SHA256 | jq -r '.pulp_href')

echo "Inspecting new file content"
pulp file content show --href $CONTENT_HREF
