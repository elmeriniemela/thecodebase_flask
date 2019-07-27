
import logging

from .dbconnect import Cursor

logger = logging.getLogger(__name__)


def insert_row(table, data_dict):
    placeholders = ', '.join(['%s'] * len(data_dict))
    columns = ', '.join(data_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
    values = list(data_dict.values())
    logger.info(sql)
    logger.info(values)
    with Cursor() as cur:
        cur.execute(sql, data_dict.values())

def update_row(table, data_dict, **search_kwargs):
    columns = ', '.join('{}=%s'.format(key) for key in data_dict.keys())
    search_columns = ', '.join('{}=%s'.format(key) for key in search_kwargs.keys())
    sql = "UPDATE %s SET %s WHERE %s" % (table, columns, search_columns)
    values = list(data_dict.values()) + list(search_kwargs.values())
    logger.info(sql)
    logger.info(values)
    with Cursor() as cur:
        cur.execute(sql, values)
