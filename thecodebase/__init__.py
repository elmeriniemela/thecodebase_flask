from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask import Markup, send_file

from content_management import Content
from dbconnect import connection

from passlib.hash import sha256_crypt
import gc
import traceback, sys, os
from functools import wraps
from datetime import datetime

TOPIC_DICT = Content()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            session['endpoint'] = request.endpoint
            return redirect(url_for('login'))

    return wrap



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
    return send_file(os.path.join(current_dir, 'docs', 'cv_elmeri.pdf'), attachment_filename='cv_elmeri.pdf')

@app.route('/eat-game/')
@login_required
def eat_game():
    return render_template("eat-game.html", game=True)

@app.route('/platform-game/')
@login_required
def platform_game():
    return render_template("platform-game.html", game=True)


def session_loggedin(username, uid):
    session['logged_in'] = True
    session['username'] = username
    session['uid'] = uid


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_username = request.form['emailUsername']
        password = request.form['password']
        c, conn = connection()

        found = c.execute("SELECT uid, username, password FROM users WHERE email=({}) OR username=({})".format(
            esc(conn, email_username), esc(conn, email_username)
        ))
        if not found:
            flash("Email/Username not registered")
            return render_template("login.html", signing=True, form=request.form)

        data = c.fetchone()
        uid, username, passwd_hash = data

        if not sha256_crypt.verify(password, passwd_hash):
            flash("Invalid password")
            return render_template("login.html", signing=True, form=request.form)


        session_loggedin(username, uid)

        flash("Succesful login!")
        endpoint = session.get('endpoint', 'homepage')
        return redirect(url_for(endpoint))

    return render_template("login.html", signing=True)

def esc(conn, string):
    return conn.escape(string.encode('utf-8')).decode('utf-8')


@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['password'])
        confirm_pass = request.form['confirmPassword']

        # If javascript validation fails
        if not sha256_crypt.verify(confirm_pass, password):
            flash("Passwords don't match!")
            return render_template("register.html", signing=True, form=request.form)

        del confirm_pass


        c, conn = connection()

        username_exists = c.execute("SELECT * FROM users WHERE username = ({})".format(esc(conn, username)))
        email_exists = c.execute("SELECT * FROM users WHERE email = ({})".format(esc(conn, email)))


        if username_exists:
            flash("Username already exists!")
            return render_template("register.html", signing=True, form=request.form)


        if email_exists:
            flash("Email already exists!")
            return render_template("register.html", signing=True, form=request.form)

        c.execute("INSERT INTO users (username, password, email, tracking) VALUES ({}, {}, {}, {})".format(
            esc(conn, username), esc(conn, password), esc(conn, email), esc(conn, '/')
        ))
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        flash("Thanks for registering!")
        session_loggedin(username, c.lastrowid)
        endpoint = session.get('endpoint', 'homepage')
        return redirect(url_for(endpoint))

    return render_template("register.html", signing=True)




@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))


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
    c, conn = connection()
    c.execute(sql, data.values())
    conn.commit()
    c.close()
    conn.close()
    gc.collect()


if __name__ == "__main__":
    app.run()
      
