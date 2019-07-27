

from flask import Blueprint
from flask import render_template
from flask import send_file

from thecodebase.lib.wrappers import login_required

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def homepage():
    return render_template("home.html", home=True)


@main.route('/my-server/')
@login_required
def my_server():
    kwargs = dict(
        my_server=True,
        bg='programming_header.jpg',
        page_title='My Server'
    )
    return render_template("my_server.html", **kwargs)


@main.route('/about-me/')
@login_required
def about_me():
    kwargs = dict(
        about_me=True,
        bg='glider_header.jpg',
        page_title='About Me'
    )
    return render_template("about_me.html", **kwargs)


@main.route('/download-cv/')
@login_required
def download_cv():
    return send_file('files/cv_elmeri.pdf', attachment_filename='cv_elmeri.pdf')
