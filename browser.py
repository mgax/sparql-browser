import os
import urllib2
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


def do_query(query):
    rows = error = None
    try:
        rows = sparql.query(ENDPOINT, query)
    except urllib2.HTTPError, e:
        if 400 <= e.code < 600:
            error = e.fp.read()
        else:
            raise
    return rows, error


@browser.route('/query')
def query():
    query = flask.request.args.get('query')

    if query:
        (rows, error) = do_query(query)
    else:
        rows = error = None

    return flask.render_template('query.html', **{
        'query': query,
        'rows': rows,
        'error': error,
    })


@browser.route('/search')
def search():
    args = {k: flask.request.args.get(k) or None for k in
            ['s', 'p', 'o', 's_regex', 'p_regex', 'o_regex']}
    query = flask.render_template('search.sparql', sparql=sparql, **args)
    (rows, error) = do_query(query)
    options = {
        'rows': rows,
        'error': error,
    }
    options.update(args)
    return flask.render_template('search.html', **options)


@browser.add_app_template_filter
def is_node(thing):
    return isinstance(thing, (sparql.IRI, sparql.BlankNode))
