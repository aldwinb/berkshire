#!/usr/bin/env bash

die() {
  >&2 echo "$@"
  exit 1
}

set -e

while [[ ${#} -gt 0 ]]; do
  opt="${1}"
  case ${opt} in
    -p|--postman-environment-file)
      postman_environment_file="${2}"
      shift;
      shift;
      ;;
    *)
      die "Usage: bash bin/run-integration-tests.bash -p postman-environment-file"
      ;;
  esac
done

# The Postman environment file is required

if [ -z "${postman_environment_file}" ]; then
  die "Usage: bash bin/run-integration-tests.bash -p postman-environment-file"
fi

# Get the absolute integration tests directory path because we're going to
# run the tests from that path
integration_tests_directory=$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)/tests/integration-tests

# If Postman environment file exists for some reason, delete it
if [ -e "postman_environment.json" ]; then
  rm ${integration_tests_directory}/postman-files/postman_environment.json
fi

# Copy Postman environment file
cp ${postman_environment_file} ${integration_tests_directory}/postman-files/postman_environment.json

# Switch directory and run test
prev=$(pwd)
test_result=0
cd ${integration_tests_directory}
docker-compose run integration-test || test_result=1
cd ${prev}

# Teardown the setup of the test
rm ${integration_tests_directory}/postman-files/postman_environment.json

exit ${test_result}
