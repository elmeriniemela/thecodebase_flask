import MySQLdb
import json
import os


def connection():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(current_dir, 'credentials.json')) as f:
        credentials = json.load(f)["mysql"]

    conn = MySQLdb.connect(
        host="localhost",
        user=credentials[0],
        passwd=credentials[1],
        db=credentials[0]
    )

    return conn.cursor(), conn
