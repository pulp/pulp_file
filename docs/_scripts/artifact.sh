#!/usr/bin/env bash

cleanup() {
  echo "Cleaning up $FILE_PATH"
  rm $FILE_PATH
}
trap cleanup EXIT

echo "Creating a dummy file to upload."
export FILE_CONTENT=$(head /dev/urandom | tr -dc a-z | head -c10)
export FILE_PATH="$(head /dev/urandom | tr -dc a-z | head -c5).txt"
echo $FILE_CONTENT > $FILE_PATH
ARTIFACT_SHA256=$(sha256sum $FILE_PATH | cut -d' ' -f1)

echo "Uploading the file to Pulp and creating an artifact"
ARTIFACT_HREF=$(pulp artifact upload --file $FILE_PATH | jq -r '.pulp_href')

echo "Inspecting new artifact."
pulp artifact show --href $ARTIFACT_HREF
