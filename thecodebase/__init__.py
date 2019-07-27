

from flask import Flask
from flask import render_template

from .lib.actions import save_endpoint
from .content import Projects
from .views import views


app = Flask(__name__)
app.register_blueprint(views)

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.context_processor
def topic_dict_context():
    return dict(TOPIC_DICT=Projects(), bg='cave_header.jpg', page_title='The Codebase')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.exception('Server Error: %s', error, extra={'stack': True})
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.exception(
        'Unhandled Exception: %s',
        error, extra={'stack': True})
    if app.debug:
        raise error
    return render_template('500.html'), 500


@app.url_value_preprocessor
def url_value_preprocessor(endpoint, values):
    """ For logging purposes, save visits to the database
    """
    if endpoint == 'static':
        return

    save_endpoint(endpoint)
