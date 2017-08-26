#!/usr/bin/env bash

# Push base image first if there's an update.
DOCKER_BASE_VERSION=$(cat base-version.txt)
export DOCKER_BERKSHIRE_DEV_IMAGE=aldwinb/berkshire-dev:${DOCKER_BASE_VERSION}
if ! docker pull ${DOCKER_BERKSHIRE_DEV_IMAGE} &> /dev/null; then
  docker build --rm -t ${DOCKER_BERKSHIRE_DEV_IMAGE} .
  docker login -u=${DOCKER_USERNAME} -p=${DOCKER_PASSWORD}
  docker push ${DOCKER_BERKSHIRE_DEV_IMAGE}
fi

if [ -n "${STDIN_OPEN}" ]; then
  docker-compose up --build -d
  docker exec -it berkshire-1 bash
else
  docker-compose up --build
fi