import flask


browser = flask.Blueprint('browser', __name__)


@browser.route('/')
def home():
    return 'hi'
