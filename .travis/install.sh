#!/usr/bin/env sh
set -v

# dev_requirements should not be needed for testing; don't install them to make sure
pip install pytest git+https://github.com/PulpQE/pulp-smash.git#egg=pulp-smash
git clone -b 3.0-dev https://github.com/pulp/pulp.git
pushd pulp/common/ && pip install -e . && popd
pushd pulp/pulpcore/ && pip install -e . && popd
pushd pulp/plugin/ && pip install -e .  && popd
pip install -e .
