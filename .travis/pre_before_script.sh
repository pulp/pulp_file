#!/usr/bin/env bash

set -euv

mkdir -p tmp/var/www/html/
mkdir -p tmp/etc/

envsubst < ../pulpcore/.travis/nginx.conf > ./tmp/etc/nginx.conf

cd ..
git clone --depth=1 https://github.com/pulp/pulp-fixtures.git
cd pulp-fixtures
for i in $(cat Makefile | grep "^fixtures\/file" | sed "s/://g"); do
    make "$i"
done
mv ./fixtures/* ../pulp_file/tmp/var/www/html/
cd ../pulp_file

nginx -c `pwd`/tmp/etc/nginx.conf

cat ../pulpcore/.travis/pulp-smash-config.json | \
    jq 'setpath(["custom","fixtures_origin"]; "http://localhost:8000/fixtures/")' > temp.json

cat temp.json > ../pulpcore/.travis/pulp-smash-config.json
