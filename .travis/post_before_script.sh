#!/usr/bin/env sh

echo "machine localhost
login admin
password password

machine 127.0.0.1
login admin
password password
" > ~/.netrc

# run pulpcore's test bindings against pulp_file
cp ../pulpcore/.travis/test_bindings.* .travis/
