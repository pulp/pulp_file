#!/usr/bin/env sh

echo "machine localhost
login admin
password admin

machine 127.0.0.1
login admin
password admin
" > ~/.netrc
