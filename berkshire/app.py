import os
import shutil
import logging
import simplejson as json

from pathlib import Path
from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.web import (Application, StaticFileHandler)

try:
    from .handlers import (PingHandler, ActivityHandler, ActivitiesHandler,
                           GroupHandler)
except ModuleNotFoundError:
    from handlers import (PingHandler, ActivityHandler, ActivitiesHandler,
                          GroupHandler)


def make_app(activity_db, group_db):
    """Creates the Tornado application.

    Args:
        activity_db: The database context used by the activity request handler.
        group_db: The database context used by the group request handler.
    Returns:
        An instance of the tornado.web.Application.
    """
    return Application([
        (r'/ping', PingHandler),
        (r'/group/([\w-]+)/activity/([\w-]+)', ActivityHandler,
         dict(db=activity_db)),
        (r'/group/([\w-]+)/activities', ActivitiesHandler, dict(db=group_db)),
        (r'/group/([\w-]+)', GroupHandler, dict(db=group_db)),
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

    # Set logging
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.getLogger('berkshiredb').setLevel(logging.DEBUG)
    logging.getLogger('handlers').setLevel(logging.DEBUG)

    # Create OpenAPI spec document
    create_openapi_spec()

    # Initialize databases

    db_options = [os.environ.get('ACTIVITY_DB'), os.environ.get('GROUP_DB')]
    dbs = {}
    for opt in db_options:
        json_opt = json.loads(opt)
        db_type = json_opt.get('type')
        db_key = json_opt.get('key')
        db_kwargs = json_opt.get('options')
        dbs[db_key] = berkshiredb.DbContext.create(db_type, **db_kwargs)

    # Add some files to the 'auto reload watch list' during development
    if os.environ['APP_ENV'] == 'local':
        watch_files(paths=['berkshire/static'])

    port = 8081
    app = make_app(activity_db=dbs['activity'],
                   group_db=dbs['group'])
    app.listen(port)
    logger.info('Starting app on 0.0.0.0:{}'.format(port))

    IOLoop.current().start()


if __name__ == "__main__":
    import berkshiredb
    main()
