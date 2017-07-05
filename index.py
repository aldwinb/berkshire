from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.web import (Application, RequestHandler, StaticFileHandler)

import os

class ActivityHandler(RequestHandler):
    def get(self, html):
        self.render('views/activity.html')

def make_app():
    return Application([
        (r'/activity/(.*)', ActivityHandler),
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
    app = make_app()
    app.listen(port)
    print('Starting app on 0.0.0.0:{}'.format(port))

    autoreload.start()
    for w in ['views', 'js']:
        for dir, _, files in os.walk(w):
            [autoreload.watch(dir + '/' + f) for f in files if
             not f.startswith('.')]

    IOLoop.current().start()
