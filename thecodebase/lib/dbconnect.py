'Context managers for MySQL cursor'

import json
import os
import gc
from contextlib import contextmanager
import MySQLdb
import pkg_resources

from ..config import CONFIG

@contextmanager
def Cursor():
    connection = MySQLdb.connect(
        host="localhost", **CONFIG['mysql'])
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as error:
        connection.rollback()
        raise error
    finally:
        cursor.close()
        connection.close()
        gc.collect()
