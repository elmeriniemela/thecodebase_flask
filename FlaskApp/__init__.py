from flask import Flask, render_template
from flask import Markup

from content_management import Content
import traceback, sys

TOPIC_DICT = Content()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

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

@app.route('/')
def homepage():
    from datetime import datetime
    date = datetime.now()
    if date.month == 12 and date.day == 6:
        return render_template("home.html", HOLIDAY=True)
    return render_template("home.html")

@app.route('/python/')
def python():
    return render_template("projects.html", TOPIC_DICT=TOPIC_DICT, key="Python")

@app.route('/c-c++/')
def c_page():
    return render_template("projects.html", TOPIC_DICT=TOPIC_DICT, key="C/C++")

@app.route('/web-development/')
def web_dev():
    return render_template("projects.html", TOPIC_DICT=TOPIC_DICT, key="Web Development")

@app.route('/java/')
def java():
    return render_template("projects.html", TOPIC_DICT=TOPIC_DICT, key="Java")

@app.route('/luottokortti/')
def luottokortti():
    return render_template("luottokortti.html")



if __name__ == "__main__":
    app.run()
      
