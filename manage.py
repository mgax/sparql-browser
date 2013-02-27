#!/usr/bin/env python

import os
import flask
from flask.ext.script import Manager

DEBUG = (os.environ.get('DEBUG') == 'on')


def create_app():
    import browser
    app = flask.Flask(__name__)
    app.debug = DEBUG
    app.register_blueprint(browser.browser)
    return app


manager = Manager(create_app)


if __name__ == '__main__':
    manager.run()
