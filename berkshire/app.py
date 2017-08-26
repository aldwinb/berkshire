from datetime import datetime
from pathlib import Path
from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.web import (Application, RequestHandler, StaticFileHandler)

import http
import os
import simplejson as json
import shutil

DATETIME_FORMAT = '%Y-%m-%dT%X'


class BaseRequestHandler(RequestHandler):
    """Serves as the base class of all the request handlers used in this
    application.

    It contains the common methods that are shared by the
    deriving request handler classes.
    """
    def __get_error_response(self, message):
        return {
            'err': message,
            'datetime': datetime.now().strftime(DATETIME_FORMAT)
        }

    def options(self, o):
        self.set_status(http.HTTPStatus.NO_CONTENT)
        self.finish()


class ActivitiesHandler(BaseRequestHandler):
    """Serves as the request handler for /activities endpoint."""
    def initialize(self, db):
        self.__db = db

    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, POST, OPTIONS')

    def get(self):
        pass

    def post(self):
        payload = json.loads(self.request.body.decode('utf-8'))
        activity_id = payload.get('activity_id')
        if not activity_id:
            self.set_status(http.HTTPStatus.INTERNAL_SERVER_ERROR)
            self.write({'error': 'Missing activity ID'})

        self.__db.upsert(id=payload['activity_id'], obj=payload)
        self.set_status(http.HTTPStatus.CREATED)
        self.write({'message': 'Success'})


class ActivityHandler(BaseRequestHandler):
    """Serves as the request handler for /activity endpoint."""
    def initialize(self, db):
        self.__db = db

    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, PUT, '
                                                         'DELETE, OPTIONS')

    def put(self, activity_id):
        payload = json.loads(self.request.body.decode('utf-8'))
        self.__db.upsert(id=activity_id, obj=payload)
        self.set_status(http.HTTPStatus.CREATED)
        self.finish()

    def get(self, activity_id):
        activity = self.__db.get(id=activity_id)
        self.set_status(http.HTTPStatus.OK)
        self.write(activity)

    def delete(self, activity_id):
        self.__db.delete(id=activity_id)
        self.set_status(http.HTTPStatus.NO_CONTENT)
        self.finish()


class PingHandler(BaseRequestHandler):
    def set_default_headers(self):
        allowed_headers = "Origin, X-Requested-With, Content-Type, Accept"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", allowed_headers)
        self.set_header('Access-Control-Allow-Methods',  'GET, OPTIONS')

    def get(self):
        self.set_status(http.HTTPStatus.OK)
        self.write({'datetime': datetime.now().strftime(DATETIME_FORMAT)})


def make_app(db):
    """Creates the Tornado application.

    Args:
        db: The database context used by the application.

    Returns:
        An instance of the tornado.web.Application.
    """
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


def watch_files(paths):
    """Adds files to the list that triggers auto reload of the application.

    Args:
        paths: The list of directories that contain the files that should be
        added to the trigger list.
    """
    autoreload.start()
    for w in paths:
        for dir, _, files in os.walk(w):
            [autoreload.watch(dir + '/' + f) for f in files if
             not f.startswith('.')]


def create_openapi_spec():
    """Creates the OpenAPI specification document of the application."""
    dirname = os.path.dirname(__file__)
    yaml_template = Path(dirname) / 'static/openapi.template.yml'
    yaml = Path(dirname) / 'static/openapi.yml'
    shutil.copyfile(yaml_template, yaml)


def main():

    # Create OpenAPI spec document
    create_openapi_spec()

    # Initialize CouchDB
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

    # Add some files to the 'auto reload watch list' during development
    if os.environ['APP_ENV'] == 'local':
        watch_files(paths=['berkshire/static'])

    IOLoop.current().start()


if __name__ == "__main__":
    import berkshiredb
    main()
