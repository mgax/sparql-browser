import os
import flask
import sparql

ENDPOINT = os.environ['SPARQL_ENDPOINT']

browser = flask.Blueprint('browser', __name__)


@browser.route('/')
def home():
    return flask.render_template('home.html')


@browser.route('/objinfo')
def objinfo():
    subject = sparql.IRI(flask.request.args['s'])
    query = flask.render_template('objinfo.sparql', **{'subject': subject})
    return flask.render_template('objinfo.html', **{
        'subject': subject,
        'rows': sparql.query(ENDPOINT, query),
    })


@browser.add_app_template_filter
def is_iri(thing):
    return isinstance(thing, sparql.IRI)
