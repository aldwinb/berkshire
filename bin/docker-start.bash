#!/usr/bin/env bash

set -ETeu -o pipefail

function cleanup() {
  docker-compose down
}

trap cleanup exit

while [[ ${#} -gt 0 ]]; do
  opt="${1}"
  case ${opt} in
    -d|--detached)
      detached=1
      shift
      ;;
    *)
      echo "Usage: bash bin/docker-start.bash [-d]"
      exit 1
      ;;
  esac
done

if [ -z "${detached+x}" ]; then
  docker-compose up --build
else
  DETACHED=1 docker-compose up --build -d
  docker exec -it berkshire-1 bash
fi
