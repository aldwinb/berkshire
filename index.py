from tornado.ioloop import IOLoop
from tornado.web import (Application, StaticFileHandler)


def make_app():
    return Application([
        (r"/(.*)", StaticFileHandler, {
            'path': 'static',
            'default_filename': 'index.html'
        }),
    ], autoreload=True)


if __name__ == "__main__":
    port = 8081
    app = make_app()
    app.listen(port)
    print('Starting app on 0.0.0.0:{}'.format(port))
    IOLoop.current().start()
