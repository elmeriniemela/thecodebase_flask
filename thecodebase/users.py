


import gc

from passlib.hash import sha256_crypt

from flask import session
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint


from thecodebase import Cursor
from thecodebase.wrappers import login_required


users = Blueprint('users', __name__, template_folder='templates')

def session_loggedin(username, uid):
    session['logged_in'] = True
    session['username'] = username
    session['uid'] = uid


@users.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_username = request.form['emailUsername']
        password = request.form['password']
        with Cursor() as cur:
            found = cur.execute("SELECT uid, username, password FROM users WHERE email=(%s) OR username=(%s)",
                (email_username, email_username,)
            )
            if not found:
                flash("Email/Username not registered")
                return render_template("login.html", signing=True, form=request.form)

            data = cur.fetchone()

        uid, username, passwd_hash = data
        if not sha256_crypt.verify(password, passwd_hash):
            flash("Invalid password")
            return render_template("login.html", signing=True, form=request.form)


        session_loggedin(username, uid)

        flash("Succesful login!")
        endpoint = session.get('endpoint', 'homepage')
        return redirect(url_for(endpoint))

    return render_template("login.html", signing=True)


@users.route('/register/', methods=["GET", "POST"])
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


        with Cursor() as cur:
            username_exists = cur.execute("SELECT * FROM users WHERE username = (%s)", (username,))
            email_exists = cur.execute("SELECT * FROM users WHERE email = (%s)", (email,))


        if username_exists:
            flash("Username already exists!")
            return render_template("register.html", signing=True, form=request.form)


        if email_exists:
            flash("Email already exists!")
            return render_template("register.html", signing=True, form=request.form)

        with Cursor() as cur:
            cur.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                (username, password, email, '/',)
            )
            uid = cur.lastrowid

        flash("Thanks for registering!")
        session_loggedin(username, uid)
        endpoint = session.get('endpoint', 'homepage')
        return redirect(url_for(endpoint))

    return render_template("register.html", signing=True)


@users.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))
    