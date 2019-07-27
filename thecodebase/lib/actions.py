
from datetime import datetime
import logging

from flask import request
from flask import session

from . import sql

logger = logging.getLogger(__name__)


def save_endpoint(endpoint):
    data = {
        'time': str(datetime.now()),
        'remote_addr': request.environ.get('HTTP_X_REAL_IP', request.environ['REMOTE_ADDR']),
    }

    if endpoint:
        data.update({'endpoint': endpoint})

    if 'logged_in' in session and 'uid' in session:
        data.update({'uid': session['uid']})

    sql.insert_row('visits', data)

