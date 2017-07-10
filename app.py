from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.web import (Application, RequestHandler, StaticFileHandler)

import berkshiredb
import os


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

    def put(self):
        pass

    def post(self):
        pass

    def get(self, activity_id):
        activity = self.__db.get(id=activity_id)
        self.write(activity)


def make_app(db):

    return Application([
        (r'/activity/(.*)', ActivityHandler, dict(db=db)),
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
    db_kwargs = {
        'host': 'http://couchdb:5984',
        'db_name': 'activity'
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
