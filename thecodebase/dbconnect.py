'Context managers for MySQL cursor'

import json
import os
import gc
from contextlib import contextmanager
import MySQLdb
import pkg_resources

filename = pkg_resources.resource_filename('thecodebase', 'credentials.json')

with open(filename) as f:
    credentials = json.load(f)["mysql"]

USER = credentials[0]
PASS = credentials[1]
MYDB = credentials[0]

@contextmanager
def Cursor():
    connection = MySQLdb.connect(
        host="localhost", user=USER, passwd=PASS, db=MYDB)
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


class NoContextlibCursor:
    '''Context manager for MySQL Cursor, that doesn't use contextlib context manager'''
    def __init__(self, host="localhost", user=USER, passwd=PASS, dbname=MYDB):

        self.connection = MySQLdb.connect(
            host=host, user=user, passwd=passwd, db=dbname)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
        gc.collect()
