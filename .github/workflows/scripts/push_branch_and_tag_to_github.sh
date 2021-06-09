#!/bin/sh
set -e

export BRANCH_NAME=$(echo $GITHUB_REF | sed -rn 's/refs\/heads\/(.*)/\1/p')

ref_string=$(git show-ref --tags | grep refs/tags/$1)

export SHA=${ref_string:0:40}

git push origin $BRANCH_NAME

curl -s -X POST https://api.github.com/repos/$GITHUB_REPOSITORY/git/refs \
-H "Authorization: token $GITHUB_TOKEN" \
-d @- << EOF
{
  "ref": "refs/tags/$1",
  "sha": "$SHA"
}
EOF
