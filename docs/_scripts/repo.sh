#!/usr/bin/env bash
export REPO_NAME=$(head /dev/urandom | tr -dc a-z | head -c5)

echo "Creating a new repository named $REPO_NAME."
pulp file repository create --name $REPO_NAME

echo "Inspecting repository."
pulp file repository show --name $REPO_NAME
