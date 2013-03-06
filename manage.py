#!/usr/bin/env python

import os
import flask
from flask.ext.script import Manager

DEBUG = (os.environ.get('DEBUG') == 'on')


def proxy_fix(app, varname='HTTP_X_FORWARDED_SCRIPT_NAME'):
    from werkzeug.contrib.fixers import ProxyFix
    hardcoded_script_name = os.environ.get('HARDCODED_SCRIPT_NAME')
    wsgi = app.wsgi_app
    def middleware(environ, start_response):
        if varname in environ:
            environ['SCRIPT_NAME'] = environ[varname]
        elif hardcoded_script_name:
            environ['SCRIPT_NAME'] = hardcoded_script_name
        return wsgi(environ, start_response)
    app.wsgi_app = ProxyFix(middleware)


def create_app():
    import browser
    app = flask.Flask(__name__)
    app.debug = DEBUG
    app.register_blueprint(browser.browser)
    if os.environ.get('REVERSE_PROXY') == 'on':
        proxy_fix(app)
    return app


manager = Manager(create_app)
if not (os.environ.get('RELOADER') == 'on'):
    manager._commands['runserver'].use_reloader = False


if __name__ == '__main__':
    manager.run()
