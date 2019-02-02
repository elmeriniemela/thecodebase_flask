from flask import Flask, render_template, send_from_directory
from flask import Markup, send_file

from content_management import Content
import traceback, sys, os

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
    return render_template("home.html", home=True)

def create_topic(topic):
    app.route('/{}/'.format(topic[1]), endpoint=topic[1])(lambda: render_template('projects.html', key=topic, projects=True))

for key in TOPIC_DICT:
    create_topic(key)

@app.route('/luottokortti/')
def luottokortti():
    return render_template("luottokortti.html")

@app.route('/my-server/')
def my_server():
    return render_template("my_server.html", my_server=True)

@app.route('/about-me/')
def about_me():
    return render_template("about_me.html", about_me=True)

@app.route('/download-cv/')
def download_cv():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return send_file(os.path.join(current_dir, 'docs', 'cv_elmeri.pdf'), attachment_filename='cv_elmeri.pdf')

@app.route('/eat-game/')
def eat_game():
    return render_template("eat-game.html", eat_game=True)

@app.route('/platform-game/')
def platform_game():
    return render_template("platform-game.html", platform_game=True)




if __name__ == "__main__":
    app.run()
      