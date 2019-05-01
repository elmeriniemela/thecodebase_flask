

import json
from datetime import datetime
import pkg_resources


from itsdangerous import (
    URLSafeSerializer,
    BadSignature,
    SignatureExpired
)

from flask import request
from flask import Blueprint
from flask import session

from thecodebase.wrappers import login_required
from thecodebase import Cursor

rest = Blueprint('rest', __name__, template_folder='templates')

CONF = pkg_resources.resource_filename('thecodebase', 'credentials.json')
with open(CONF) as f:
    KEY = json.load(f)["secret_key"]

@rest.route('/notes', methods=['get'])
def notes():
    """
    curl https://www.thecodebase.site/notes
    """
    select_sql = """
    SELECT note FROM Notes
    """
    with Cursor() as cur:
        cur.execute(select_sql)
        data = cur.fetchall()
    data = "\n".join([t[0] for t in data])
    return data + '\n'

@rest.route('/add_note/', methods=['POST'])
def add_note():
    """
    curl -u <token>:unused -X POST -F "note=<command>" https://www.thecodebase.site/add_note/
    """
    if request.authorization and verify_auth_token(request.authorization.get('username')):
        note = request.form.get('note')
        if note:
            with Cursor() as cur:
                cur.execute("INSERT INTO Notes (note, time) VALUES (%s, %s)", 
                    (note, datetime.now(),)
                )
            return "OK\n"
        else:
            return "Empty post\n"
        
    return "Authorization failed\n"


@rest.route('/get-token/')
@login_required
def encode_auth_token():
    """
    Generates the Auth Token
    :return: string
    """
    auth_s = URLSafeSerializer(KEY)
    token = auth_s.dumps({"uid": session.get('uid')})
    return token

def verify_auth_token(token):
    s = URLSafeSerializer(KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    return data['uid']
