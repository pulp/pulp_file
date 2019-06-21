#!/bin/bash

pip install twine

django-admin runserver 24817 >> ~/django_runserver.log 2>&1 &
sleep 5

cd /home/travis/build/pulp/pulp_file/
export REPORTED_VERSION=$(http :24817/pulp/api/v3/status/ | jq --arg plugin pulp_file -r '.versions[] | select(.component == $plugin) | .version')
export DESCRIPTION="$(git describe --all --exact-match `git rev-parse HEAD`)"
if [[ $DESCRIPTION == 'tags/'$REPORTED_VERSION ]]; then
  export VERSION=${REPORTED_VERSION}
else
  export EPOCH="$(date +%s)"
  export VERSION=${REPORTED_VERSION}.${EPOCH}
fi

export response=$(curl --write-out %{http_code} --silent --output /dev/null https://pypi.org/project/pulp-file-client/$VERSION/)

if [ "$response" == "200" ];
then
    exit
fi

cd
git clone https://github.com/pulp/pulp-openapi-generator.git
cd pulp-openapi-generator

./generate.sh pulp_file python $VERSION
cd pulp_file-client
python setup.py sdist bdist_wheel --python-tag py3
twine upload dist/* -u pulp -p $PYPI_PASSWORD
exit $?
