#!/usr/bin/env bash

echo "Kick off a task to add content to a repository, storing TASK_URL env variable"
pulp file repository add --name $REPO_NAME --sha256 $ARTIFACT_SHA256 --relative-path "test_upload.txt"

echo "Inspecting repository version."
pulp file repository version show --repository $REPO_NAME --version 1
