#!/bin/bash

openssl aes-256-cbc -K $encrypted_3d576e61f0ca_key -iv $encrypted_3d576e61f0ca_iv -in .travis/credentials.enc -out ~/.gem/credentials -d
sudo chmod 600 ~/.gem/credentials

django-admin runserver 24817 >> ~/django_runserver.log 2>&1 &
sleep 5

cd /home/travis/build/pulp/pulp_file/
COMMIT_SHA="$(git rev-parse HEAD | cut -c1-8)"
export COMMIT_SHA

cd

git clone https://github.com/pulp/pulp-swagger-codegen.git
cd pulp-swagger-codegen


sudo ./generate.sh pulp_file ruby $COMMIT_SHA
sudo chown travis:travis pulp_file-client
cd pulp_file-client
gem build pulp_file_client
GEM_FILE="$(ls | grep pulp_file_client-)"
gem push ${GEM_FILE}
