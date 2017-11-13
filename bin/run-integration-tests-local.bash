#!/usr/bin/env bash

set -ETeu -o pipefail

integration_tests_directory=$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)/tests/integration-tests
postman_env_file_target=${integration_tests_directory}/postman-files/postman_environment.json

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
Usage: bash bin/run-integration-tests-local.bash -p postman-environment-file
EOF
}

function run_integration_tests() {

  # If Postman environment file exists for some reason, delete it
  if [[ -e ${postman_env_file_target} ]]; then
    cleanup
  fi

  # Copy Postman environment file
  cp ${postman_environment_file} ${postman_env_file_target}

  docker-compose -f docker-compose-test.yml \
  -p berkshire-test \
  run integration-test || exit 1
}

function cleanup() {
  rm ${postman_env_file_target}
  docker-compose -f docker-compose-test.yml \
  -p berkshire-test \
  down
}

#######################################
#
# main
#
#######################################
if [[ ${#} -eq 0 ]]; then
  die $(usage)
fi

while [[ ${#} -gt 0 ]]; do
  opt="${1}"
  case ${opt} in
    -p|--postman-environment-file)
      postman_environment_file="${2}"
      shift;
      shift;
      ;;
    *)
      die $(usage)
      ;;
  esac
done

if [ -z "${postman_environment_file}" ]; then
  die $(usage)
fi

trap cleanup EXIT
run_integration_tests || exit 1
