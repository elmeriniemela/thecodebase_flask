

import json
from datetime import datetime

from flask import session
from flask import request
from flask import Blueprint


from thecodebase import Cursor

ajax = Blueprint('ajax', __name__, template_folder='templates')

@ajax.route('/post-score', methods=['POST'])
def post_score():
    score = request.form['score']
    select_sql = """
    SELECT username, score, time FROM Score
    JOIN users ON users.uid = Score.uid
    ORDER BY score DESC
    """
    with Cursor() as cur:
        cur.execute("INSERT INTO Score (score, uid, time) VALUES (%s, %s, %s)", 
            (score, session.get('uid'), datetime.now(),)
        )
        cur.execute(select_sql)
        data = cur.fetchmany(10)

    data_list = []
    for line in data:
        username, score, date = line
        data_list.append([username.replace('ä', 'a').replace('ö', 'o'), score, str(date)])

    return json.dumps(data_list)