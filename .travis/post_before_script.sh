#!/usr/bin/env sh

echo "machine pulp
login admin
password password
" > ~/.netrc

export BASE_ADDR=http://pulp:80