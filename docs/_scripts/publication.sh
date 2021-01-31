#!/usr/bin/env bash
echo "Create a new publication specifying the repository_version."
PUBLICATION_HREF=$(pulp file publication create --repository $REPO_NAME --version 1 | jq -r '.pulp_href')

echo "Inspecting Publication."
pulp show --href $PUBLICATION_HREF
