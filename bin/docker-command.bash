#!/usr/bin/env bash

set -e

until wget --spider http://couchdb:5984/_utils &> /dev/null; do
  >&2 echo "CouchDB is unavailable - sleeping"
  sleep 1
done

>&2 echo "CouchDB is up - executing command"

python dbsetup.py

if [ "${DETACHED}" -eq "1" ]; then
  tail -f /dev/null
else
  python berkshire/app.py
fi
