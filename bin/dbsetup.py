import couchdb
import os
import simplejson as json
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def setup_db(type, **kwargs):
    if type == 'couchdb':
        setup_couch_db(**kwargs)


def setup_couch_db(host, db_name):
    server = couchdb.Server(host, )
    if db_name not in server:
        server.create(db_name)


def setup_dbs():
    options = [os.environ.get('ACTIVITY_DB'), os.environ.get('GROUP_DB')]
    for opt in options:
        json_opt = json.loads(opt)
        db_type = json_opt.get('type')
        setup_db(type=db_type, **json_opt.get('options'))


def main():
    setup_dbs()


if __name__ == '__main__':
    main()
