import couchdb
import os


def setup_dbs():
    host = os.environ['COUCHDB_HOST']
    activity_db_name = os.environ['COUCHDB_ACTIVITY_DB']
    server = couchdb.Server(host, )
    if activity_db_name not in server:
        server.create(activity_db_name)


def main():
    setup_dbs()


if __name__ == '__main__':
    main()
