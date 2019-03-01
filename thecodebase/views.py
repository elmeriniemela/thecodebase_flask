

import os

from flask import render_template
from flask import send_file

from thecodebase import app
from thecodebase import TOPIC_DICT
from thecodebase.wrappers import login_required, mobile_not_supported


@app.route('/')
def homepage():
    return render_template("home.html", home=True)

def create_topic(topic):
    kwargs = dict(
        key=topic, 
        projects=True, 
        bg='programming_header.jpg',
        page_title='Projects'
    )
    app.route('/{}/'.format(topic[1]), endpoint=topic[1])(login_required(lambda: render_template('projects.html', **kwargs)))

for key in TOPIC_DICT:
    create_topic(key)


@app.route('/my-server/')
@login_required
def my_server():
    kwargs = dict(
        my_server=True, 
        bg='programming_header.jpg', 
        page_title='My Server'
    )
    return render_template("my_server.html", **kwargs)

@app.route('/about-me/')
@login_required
def about_me():
    kwargs = dict(
         about_me=True, 
         bg='glider_header.jpg',
         page_title='About Me'
    )
    return render_template("about_me.html", **kwargs)

@app.route('/download-cv/')
@login_required
def download_cv():
    import pkg_resources
    filename = pkg_resources.resource_filename('thecodebase', 'docs/cv_elmeri.pdf')
    return send_file(filename, attachment_filename='cv_elmeri.pdf')

@app.route('/eat-game/')
@login_required
@mobile_not_supported
def eat_game():
    kwargs = dict(
         game=True,
         bg='gaming_header.jpg',
         page_title='Eat Game'
    )
    return render_template("eat-game.html", **kwargs)

@app.route('/platform-game/')
@login_required
@mobile_not_supported
def platform_game():
    kwargs = dict(
         game=True,
         bg='gaming_header.jpg',
         page_title='Platform Game'
    )
    return render_template("platform-game.html", **kwargs)
