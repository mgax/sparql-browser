#!/usr/bin/env python

import flask
from flask.ext.script import Manager


def create_app():
    import browser
    app = flask.Flask(__name__)
    app.register_blueprint(browser.browser)
    return app


manager = Manager(create_app)


if __name__ == '__main__':
    manager.run()
