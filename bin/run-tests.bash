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

function run_unit_tests() {
  docker-compose -f docker-compose-test.yml \
  -p berkshire-test \
  run app tox || exit 1
}

function run_integration_tests() {
  bash bin/run-integration-tests-local.bash -p ${postman_environment_file}
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

run_unit_tests || exit 1
run_integration_tests || exit 1
