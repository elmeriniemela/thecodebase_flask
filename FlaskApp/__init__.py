from flask import Flask, render_template
from flask import make_response

from content_management import Content
import traceback, sys

TOPIC_DICT = Content()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def format_exception(tb):
    res = make_response(tb.render_as_text())
    res.content_type = 'text/plain'
    return res

app.jinja_env.exception_formatter = format_exception

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/python/')
def python():
    return render_template("python.html", TOPICS=TOPIC_DICT["Python"])

@app.route('/c-c++/')
def c_page():
    return render_template("c_pagec.html", TOPICS=TOPIC_DICT["Python"])

@app.route('/luottokortti/')
def luottokortti():
    return render_template("luottokortti.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def python_error(e):
    _, _, tb = sys.exc_info()
    return render_template("500.html", error=repr(e), traceback=traceback.format_tb(tb))

if __name__ == "__main__":
    app.run()
      
