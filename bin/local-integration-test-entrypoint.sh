#!/usr/bin/env sh

set -eu -o pipefail

until wget -s http://app:8081 &> /dev/null; do
  >&2 echo "Berkshire app is unavailable - sleeping"
  sleep 1
done

>&2 echo "Berkshire app is up - running tests"

newman run berkshire-api.postman_collection.json \
  -e postman_environment.json \
  -d berkshire-api.postman_data.json || exit 1
