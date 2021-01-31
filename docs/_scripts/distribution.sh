#!/usr/bin/env bash

export DIST_NAME=$(head /dev/urandom | tr -dc a-z | head -c5)
export DIST_BASE_PATH=$(head /dev/urandom | tr -dc a-z | head -c5)

# Distributions are created asynchronously.
echo "Creating distribution \
  (name=$DIST_NAME, base_path=$DIST_BASE_PATH publication=$PUBLICATION_HREF)."
pulp file distribution create \
  --name $DIST_NAME \
  --base-path $DIST_BASE_PATH \
  --publication $PUBLICATION_HREF

echo "Inspecting Distribution."
pulp file distribution show --name $DIST_NAME
