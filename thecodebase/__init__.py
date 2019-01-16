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

@app.context_processor
def topic_dict_context():
    return dict(TOPIC_DICT=TOPIC_DICT)


@app.route('/')
def homepage():
    return render_template("home.html")

def create_project(topic):
    app.route('/{}/'.format(topic[1]), endpoint=topic[1])(lambda: render_template('projects.html', key=topic))

for key in TOPIC_DICT.keys():
    create_project(key)

@app.route('/luottokortti/')
def luottokortti():
    return render_template("luottokortti.html")

@app.route('/my-server/')
def my_server():
    return render_template("my_server.html")

@app.route('/about-me/')
def about_me():
    return render_template("about_me.html")




if __name__ == "__main__":
    app.run()
      
