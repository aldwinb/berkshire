import os

import simplejson as json
from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.web import (Application, RequestHandler, StaticFileHandler)

from berkshire import berkshiredb


class ActivitiesHandler(RequestHandler):
    def initialize(self, db):
        self.__db = db

    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, PUT, POST, '
                                                         'OPTIONS')

    def options(self, o):
        self.set_status(204)
        self.finish()

    def get(self):
        pass

    def post(self):
        payload = json.loads(self.request.body.decode('utf-8'))
        activity_id = payload.get('activity_id')
        if not activity_id:
            self.set_status(500)
            self.write({'error': 'Missing activity ID'})

        self.__db.upsert(id=payload['activity_id'], obj=payload)
        self.set_status(200)
        self.write({'message': 'Success'})


class ActivityHandler(RequestHandler):

    def initialize(self, db):
        self.__db = db

    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, PUT, POST, '
                                                         'OPTIONS')

    def options(self, o):
        self.set_status(204)
        self.finish()

    def put(self, activity_id):
        payload = json.loads(self.request.body.decode('utf-8'))
        self.__db.upsert(id=activity_id, obj=payload)
        self.set_status(200)
        self.write({'message': 'Success'})

    def get(self, activity_id):
        activity = self.__db.get(id=activity_id)
        self.set_status(200)
        self.write(activity)


def make_app(db):

    return Application([
        (r'/activity/(\w+)', ActivityHandler, dict(db=db)),
        (r'/js/(.*)', StaticFileHandler, {
            'path': 'js'
        }),
        (r'/(.*)', StaticFileHandler, {
            'path': 'views',
            'default_filename': 'index.html'
        }),
    ], )


if __name__ == "__main__":
    port = 8081
    couchdb_host = os.environ['COUCHDB_HOST']
    activity_db_name = os.environ['COUCHDB_ACTIVITY_DB']
    db_kwargs = {
        'host': couchdb_host,
        'db_name': activity_db_name
    }
    app = make_app(db=berkshiredb.DbContext.create('1', **db_kwargs))
    app.listen(port)
    print('Starting app on 0.0.0.0:{}'.format(port))

    autoreload.start()
    for w in ['views', 'js']:
        for dir, _, files in os.walk(w):
            [autoreload.watch(dir + '/' + f) for f in files if
             not f.startswith('.')]

    IOLoop.current().start()
