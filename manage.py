#!/usr/bin/env python

import flask
from flask.ext.script import Manager


def create_app():
    app = flask.Flask(__name__)

    @app.route('/')
    def home():
        return 'hi'

    return app


manager = Manager(create_app)


if __name__ == '__main__':
    manager.run()
