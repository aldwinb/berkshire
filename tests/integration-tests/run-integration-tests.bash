#!/usr/local/bin/bash

die() {
  >&2 echo "$@"
  exit 1
}

set -e

# The Postman environment file is required
postman_environment_file="${1}"
if [ -z "${postman_environment_file}" ]; then
  die "Postman environment file required"
fi

# Get the absolute integration tests directory path because we're going to
# run the tests from that path
integration_tests_directory=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
prev=$(pwd)
cd ${integration_tests_directory}

# If Postman environment file exists for some reason, delete it
if [ -e "postman_environment.json" ]; then
  rm postman-files/postman_environment.json
fi

# Copy Postman environment file
cp ${postman_environment_file} postman-files/postman_environment.json

test_result=0
docker-compose run integration-test || test_result=1

# Teardown the setup of the test
rm postman-files/postman_environment.json
cd ${prev}

exit ${test_result}
