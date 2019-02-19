
import gc
import traceback
import sys
from datetime import datetime

from passlib.hash import sha256_crypt

from flask import Flask
from flask import render_template
from flask import Markup
from flask import session
from flask import request


from .content_management import Content
from .dbconnect import Cursor
from .users import users
from .ajax import ajax

TOPIC_DICT = Content()

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(ajax)

app.config['TEMPLATES_AUTO_RELOAD'] = True

import thecodebase.views

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def python_error(e):
    _, _, tb = sys.exc_info()
    return render_template("500.html", error=repr(e), traceback=traceback.format_tb(tb))

def format_exception(tb):
    error_html = Markup(tb.render_as_text())
    return render_template("jinja_error.html", error=error_html)

app.jinja_env.exception_formatter = format_exception

@app.context_processor
def topic_dict_context():
    return dict(TOPIC_DICT=TOPIC_DICT)


@app.url_value_preprocessor
def url_value_preprocessor(endpoint, values):
    if endpoint == 'static':
        return

    data = {
        'time': str(datetime.now()),
        'remote_addr': request.environ.get('HTTP_X_REAL_IP', request.environ['REMOTE_ADDR']),
    }

    if endpoint:
        data.update({'endpoint': endpoint})

    if 'logged_in' in session and 'uid' in session:
        data.update({'uid': session['uid']})

    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('visits', columns, placeholders)

    with Cursor() as cur:
        cur.execute(sql, data.values())

if __name__ == "__main__":
    app.run()
      
