

import os

from flask import render_template
from flask import send_file

from thecodebase import app
from thecodebase import TOPIC_DICT
from thecodebase.wrappers import login_required


@app.route('/')
def homepage():
    return render_template("home.html", home=True)

def create_topic(topic):
    app.route('/{}/'.format(topic[1]), endpoint=topic[1])(login_required(lambda: render_template('projects.html', key=topic, projects=True)))

for key in TOPIC_DICT:
    create_topic(key)


@app.route('/my-server/')
@login_required
def my_server():
    return render_template("my_server.html", my_server=True)

@app.route('/about-me/')
@login_required
def about_me():
    return render_template("about_me.html", about_me=True)

@app.route('/download-cv/')
@login_required
def download_cv():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return send_file(
        os.path.join(current_dir, 'docs', 'cv_elmeri.pdf'),
        attachment_filename='cv_elmeri.pdf'
    )

@app.route('/eat-game/')
@login_required
def eat_game():
    return render_template("eat-game.html", game=True)

@app.route('/platform-game/')
@login_required
def platform_game():
    return render_template("platform-game.html", game=True)
