from datetime import datetime
from pathlib import Path
from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.web import (Application, RequestHandler, StaticFileHandler)

import inspect
import os
import simplejson as json
import shutil


class BaseRequestHandler(RequestHandler):

    def get_error_response(self, message):
        return {
            'status': 'Error',
            'message': message,
            'datetime': datetime.now().strftime('%Y-%m-%dT%X')
        }

    def get_201_response(self):
        return {
            'status': 'Success',
            'datetime': datetime.now().strftime('%Y-%m-%dT%X')
        }


class ActivitiesHandler(BaseRequestHandler):
    def initialize(self, db):
        self.__db = db

    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, POST, OPTIONS')

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


class ActivityHandler(BaseRequestHandler):

    def initialize(self, db):
        self.__db = db

    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, PUT, '
                                                         'DELETE, OPTIONS')

    def options(self, o):
        self.set_status(204)
        self.finish()

    def put(self, activity_id):
        payload = json.loads(self.request.body.decode('utf-8'))
        self.__db.upsert(id=activity_id, obj=payload)
        self.set_status(201)
        self.write(self.get_201_response())

    def get(self, activity_id):
        activity = self.__db.get(id=activity_id)
        self.set_status(200)
        self.write(activity)

    def delete(self, activity_id):
        self.__db.delete(id=activity_id)
        self.set_status(204)
        self.finish()


class PingHandler(BaseRequestHandler):
    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, OPTIONS')

    def options(self, o):
        self.set_status(204)
        self.finish()

    def get(self):
        self.set_status(200)
        self.write('Hello')


def make_app(db):

    return Application([
        (r'/ping', PingHandler),
        (r'/activity/(\w+)', ActivityHandler, dict(db=db)),
        (r'/js/(.*)', StaticFileHandler, {
            'path': 'js'
        }),
        (r'/(.*)', StaticFileHandler, {
            'path': 'berkshire/static',
            'default_filename': 'index.html'
        }),
    ], )


def main():

    pre_path = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    yaml_template = Path(pre_path) / 'static/openapi.template.yaml'
    yaml = Path(pre_path) / 'static/openapi.yaml'
    shutil.copyfile(yaml_template, yaml)

    couchdb_host = os.environ['COUCHDB_HOST']
    activity_db_name = os.environ['COUCHDB_ACTIVITY_DB']
    db_kwargs = {
        'host': couchdb_host,
        'db_name': activity_db_name
    }

    port = 8081
    app = make_app(db=berkshiredb.DbContext.create('1', **db_kwargs))
    app.listen(port)
    print('Starting app on 0.0.0.0:{}'.format(port))

    autoreload.start()
    for w in ['berkshire/static']:
        for dir, _, files in os.walk(w):
            [autoreload.watch(dir + '/' + f) for f in files if
             not f.startswith('.')]

    IOLoop.current().start()


if __name__ == "__main__":
    import berkshiredb
    main()
