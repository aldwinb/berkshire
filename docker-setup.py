import couchdb
import os
import sys

def setup_dbs():
    args = sys.argv[1:]
    host = os.environ['COUCHDB_HOST']
    activity_db_name = os.environ['APP_ACTIVITY_DATABASE']
    server = couchdb.Server(host, )
    if activity_db_name not in server:
        server.create(activity_db_name)


def main():
    setup_dbs()


if __name__ == '__main__':
    main()