


import json
from datetime import datetime

from flask import session
from flask import render_template
from flask import send_file
from flask import request
from flask import flash

from thecodebase import app
from thecodebase import TOPIC_DICT
from thecodebase.wrappers import login_required, mobile_not_supported

from .content import Games
from .dbconnect import Cursor
from .refactor_ics import refactor_file

GAMES_DICT = Games()


from .admin import get_repos



@app.route('/github-projects/')
@login_required
def github_projects():
    kwargs = dict(
        repos=get_repos(),
        projects=True,
        bg='programming_header.jpg',
        page_title='Github Projects'
    )
    return render_template("github.html", **kwargs)


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
    app.route('/{}/'.format(topic.url), endpoint=topic.url)(
        login_required(lambda: render_template('projects.html', **kwargs))
    )

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


def refactor_template():
    
    with Cursor() as cur:
        found = cur.execute("SELECT json FROM Refactor ORDER BY time DESC")
        if found:
            data = json.loads(cur.fetchone()[0].decode('utf-8', 'ignore'))
            lines = [(key, value) for key, value in data.items()]
        else:
            lines = []

    kwargs = dict(
        refactor=True, 
        bg='programming_header.jpg', 
        page_title='Refactor ICS',
        enumerate=enumerate,
        lines=lines,
    )
    return render_template("refactor-ics.html", **kwargs)

@app.route('/refactor-ics/', methods=['GET', 'POST'])
@login_required
def refactor_ics():
    if request.method == 'POST':
        if 'ics-file' not in request.files:
            flash('Select file first')
            return refactor_template()
        
        ics_file = request.files['ics-file']
        if ics_file.filename == '' or not ics_file.filename.endswith('.ics'):
            flash('Select proper filename (.ics)')
            return refactor_template()

        if ics_file:
            try:
                file_io, results = refactor_file(ics_file)
                with Cursor() as cur:
                    cur.execute("INSERT INTO Refactor (json, uid, time) VALUES (%s, %s, %s)",
                        (json.dumps(results, ensure_ascii=False).encode('utf-8'), session.get('uid'), datetime.now(),)
                    )
                return send_file(file_io, attachment_filename="refactored.ics", as_attachment=True)
            except ValueError as error:
                app.logger.error("Error processing ics-file: {}\n\nFile content:\n{}".format(error, ics_file.read()))
                flash("Error: Corrupted file")
            
    return refactor_template()

    

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
    return send_file('docs/cv_elmeri.pdf', attachment_filename='cv_elmeri.pdf')
