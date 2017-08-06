#!/usr/local/bin/bash

set -e

host="{$1}"

until wget --spider http://couchdb:5984/_utils &> /dev/null; do
  >&2 echo "CouchDB is unavailable - sleeping"
  sleep 1
done

>&2 echo "CouchDB is up - executing command"

python docker-setup.py
if [ -n "$STDIN_OPEN" ]; then
  tail -f /dev/null
else
  python berkshire/app.py
fi
