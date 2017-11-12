#!/usr/bin/env bash

set -ETeu -o pipefail

#######################################
#
# Prints a message then exits with a non-zero code.
#
#######################################
function die() {
  >&2 echo "$@"
  exit 1
}

#######################################
#
# Echoes the usage instructions of the script.
#
#######################################
function usage() {
  cat <<EOF
Usage: bash bin/run-tests.bash -p postman-environment-file
EOF
}

function run_integration_tests() {
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

}

postman_environment_file=
#######################################
#
# main
#
#######################################
while [[ ${#} -gt 0 ]]; do
  opt="${1}"
  case ${opt} in
    -p|--postman-environment-file)
      postman_environment_file="${2}"
      shift;
      shift;
      ;;
    *)
      die usage
      ;;
  esac
done

if [ -z "${postman_environment_file}" ]; then
  die $(usage)
fi

run_integration_tests || exit 1
