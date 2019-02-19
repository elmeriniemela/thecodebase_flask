



from functools import wraps

from flask import session
from flask import request
from flask import flash
from flask import Markup
from flask import redirect
from flask import url_for

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            message = Markup('You need to login first. New user? Register <a href="/register/">here.</a> It only takes a few seconds.')
            flash(message)
            if request.endpoint not in ['login', 'register']:
                session['endpoint'] = request.endpoint
            else:
                session['endpoint'] = session.get('endpoint', 'homepage')
            return redirect(url_for('login'))

    return wrap