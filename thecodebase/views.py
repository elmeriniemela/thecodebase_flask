

import os

from flask import render_template
from flask import send_file
from flask import request
from flask import flash

from thecodebase import app
from thecodebase import TOPIC_DICT
from thecodebase.wrappers import login_required, mobile_not_supported

from .content import Games
from .refactor_ics import refactor_file

GAMES_DICT = Games()


@app.route('/')
def homepage():
    return render_template("home.html", home=True)

def create_topic(topic):
    kwargs = dict(
        topic=topic,
        projects=True,
        bg='programming_header.jpg',
        page_title='Projects'
    )
    app.route('/{}/'.format(topic.url), endpoint=topic.url)(login_required(lambda: render_template('projects.html', **kwargs)))

for key in TOPIC_DICT:
    create_topic(key)


@app.route('/games/')
def games():
    kwargs = dict(
        game=True,
        bg='gaming_header.jpg',
        GAMES_DICT=GAMES_DICT,
        page_title='Games'
    )
    return render_template("games.html", **kwargs)

def create_game(game, resources):
    kwargs = dict(
         game=True,
         bg='gaming_header.jpg',
         page_title=game.title,
         folder=game.url,
         resources=resources
    )
    app.route('/games/{}/'.format(game.url), endpoint=game.url)(
        mobile_not_supported(
                login_required(
                    lambda: render_template('phaser-game.html', **kwargs)
                )
            )
        )

for game, resources in GAMES_DICT.items():
    create_game(game, resources)


@app.route('/my-server/')
@login_required
def my_server():
    kwargs = dict(
        my_server=True, 
        bg='programming_header.jpg', 
        page_title='My Server'
    )
    return render_template("my_server.html", **kwargs)


@app.route('/refactor-ics/', methods=['GET', 'POST'])
@login_required
def refactor_ics():
    kwargs = dict(
        refactor=True, 
        bg='programming_header.jpg', 
        page_title='Refactor ICS'
    )

    def allowed_file(filename):
        allowed = '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['ics'])
        if not allowed:
            flash("Filetype not allowed")
        return allowed

    if request.method == 'POST':
        if 'ics-file' not in request.files:
            flash('Select file first')
            return render_template("refactor-ics.html", **kwargs)
        
        ics_file = request.files['ics-file']
        if ics_file.filename == '':
            flash('Select proper filename')
            return render_template("refactor-ics.html", **kwargs)

        if ics_file and allowed_file(ics_file.filename):
            file_io = refactor_file(ics_file)
            return send_file(file_io, attachment_filename="refactored.ics", as_attachment=True)

    return render_template("refactor-ics.html", **kwargs)

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


