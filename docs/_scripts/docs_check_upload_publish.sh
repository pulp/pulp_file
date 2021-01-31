#!/usr/bin/env bash

# This script will execute the component scripts and ensure that the documented examples
# work as expected.

# NOTE: These scripts use httpie and requires a .netrc for authentication with Pulp

# From the _scripts directory, run with `source docs_check_upload_publish.sh` (source to preserve
# the environment variables)
source setup.sh

source repo.sh
source artifact.sh
source content.sh
source add_remove.sh

source publication.sh
source distribution.sh
source download_after_upload.sh

source exporter.sh
source export.sh
