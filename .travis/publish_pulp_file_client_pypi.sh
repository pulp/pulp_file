#!/bin/bash

pip install twine

django-admin runserver 24817 >> ~/django_runserver.log 2>&1 &
sleep 5

cd /home/travis/build/pulp/pulp_file/
export REPORTED_VERSION=$(http :24817/pulp/api/v3/status/ | jq --arg plugin pulp_file -r '.versions[] | select(.component == $plugin) | .version')
export COMMIT_COUNT="$(git rev-list ${REPORTED_VERSION}^..HEAD | wc -l)"
export VERSION=${REPORTED_VERSION}.dev.${COMMIT_COUNT}

cd
git clone https://github.com/pulp/pulp-swagger-codegen.git
cd pulp-swagger-codegen

sudo ./generate.sh pulp_file python $VERSION
sudo chown -R travis:travis pulp_file-client
cd pulp_file-client
python setup.py sdist bdist_wheel --python-tag py3
twine upload dist/* -u pulp -p $PYPI_PASSWORD
exit $?
