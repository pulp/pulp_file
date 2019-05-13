#!/bin/bash

openssl aes-256-cbc -K $encrypted_3d576e61f0ca_key -iv $encrypted_3d576e61f0ca_iv -in .travis/credentials.enc -out ~/.gem/credentials -d
sudo chmod 600 ~/.gem/credentials

django-admin runserver 24817 >> ~/django_runserver.log 2>&1 &
sleep 5

cd /home/travis/build/pulp/pulp_file/
export REPORTED_VERSION=$(http :24817/pulp/api/v3/status/ | jq --arg plugin pulp_file -r '.versions[] | select(.component == $plugin) | .version')
export EPOCH="$(date +%s)"
export VERSION=${REPORTED_VERSION}.dev.${EPOCH}

export response=$(curl --write-out %{http_code} --silent --output /dev/null https://rubygems.org/gems/pulp_file_client/versions/$VERSION)

if [ "$response" == "200" ];
then
    exit
fi

cd
git clone https://github.com/pulp/pulp-openapi-generator.git
cd pulp-openapi-generator

sudo ./generate.sh pulp_file ruby $VERSION
sudo chown -R travis:travis pulp_file-client
cd pulp_file-client
gem build pulp_file_client
GEM_FILE="$(ls | grep pulp_file_client-)"
gem push ${GEM_FILE}
