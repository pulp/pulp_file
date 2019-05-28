#!/usr/bin/env sh
set -v

mkdir -p ~/.config/pulp_smash
cp ../pulpcore/.travis/pulp-smash-config.json ~/.config/pulp_smash/settings.json

echo "machine localhost
login admin
password admin

machine 127.0.0.1
login admin
password admin
" > ~/.netrc
