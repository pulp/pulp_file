#!/usr/bin/env sh

echo "Creating a dummy file at path FILE_CONTENT to upload."
export FILE_CONTENT=$(head /dev/urandom | tr -dc a-z | head -c10)
echo $FILE_CONTENT > test_upload.txt

echo "Uploading the file to Pulp, creating an artifact, storing ARTIFACT_HREF."
export ARTIFACT_HREF=$(http --form POST $BASE_ADDR/pulp/api/v3/artifacts/ \
    file@./test_upload.txt \
    | jq -r '._href')

echo "Inspecting new artifact."
http $BASE_ADDR$ARTIFACT_HREF
