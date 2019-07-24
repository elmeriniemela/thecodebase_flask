

def add_column(table, column, datatype, position):
    from thecodebase.dbconnect import Cursor
    test_sql = """
    SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA ='thecodebase' 
    AND TABLE_NAME = %s 
    AND COLUMN_NAME = %s;
    """
    alter = "ALTER TABLE %s ADD COLUMN %s %s " % (table, column, datatype)
    if position:
        alter += position
    with Cursor() as cur:
        exists = cur.execute(test_sql, (table, column,))
        if not exists:
            print("CHANGED: Adding column: %s" % alter)
            cur.execute(alter)


def init_database():
    from thecodebase.dbconnect import Cursor
    tables = {
        'users': """
            CREATE TABLE users (
                uid INT(11) AUTO_INCREMENT PRIMARY KEY, 
                username VARCHAR(20), 
                password VARCHAR(100), 
                email VARCHAR(50), 
                settings TEXT(32500), 
                tracking TEXT(32500),
                auth_token VARCHAR(100),
                rank INT(3)
            );
            """,

        'visits': """
            CREATE TABLE visits (
                visit_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                uid INT,
                time DATETIME,
                remote_addr VARCHAR(45),
                endpoint VARCHAR(50),
                FOREIGN KEY (uid) REFERENCES users(uid)
            );
            """,

        'Score': """
            CREATE TABLE Score (
                score_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                uid INT,
                time DATETIME,
                score INT,
                FOREIGN KEY (uid) REFERENCES users(uid)
            );
            """,

        'Refactor': """
            CREATE TABLE Refactor (
                refactor_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                uid INT,
                time DATETIME,
                json LONGBLOB,
                FOREIGN KEY (uid) REFERENCES users(uid)
            );
            """,

        'Notes': """
            CREATE TABLE Notes (
                note_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                time DATETIME,
                note TEXT
            );
            """,

    }

    new_columns = [
        ('users', 'auth_token', 'VARCHAR(100)', 'AFTER tracking')
    ]

    test_sql = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'thecodebase'
    AND table_name = %s;
    """
    created = []
    with Cursor() as cur:
        for table, query in tables.items():
            table_exists = cur.execute(test_sql, (table, ))
            if not table_exists:
                cur.execute(query)
                created.append(table)
        for column in new_columns:
            add_column(*column)

    if created:
        print("CHANGED: Created new tables: {}".format(', '.join(created)))
    else:
        print("OK")

def init_config():
    import pkg_resources
    import json
    import os
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits
    filename = pkg_resources.resource_filename('thecodebase', 'config.json')
    config = {
        "mysql":{
            "db": "thecodebase",
            "user": "thecodebase",
            "passwd": ''.join(secrets.choice(alphabet) for i in range(20)),
        },
        "secret_key": ''.join(secrets.choice(alphabet) for i in range(20)),
    }

    log_path = '/var/log/uwsgi'
    if os.path.isdir(log_path):
        config['log_file'] = os.path.join(log_path, 'thecodebase-flask.log')

    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)
    
    print("Config created")
    from thecodebase.config import cache_config
    cache_config()


def setup_mysql(passwd=None):
    import MySQLdb
    kwargs = dict(
        host='localhost', user='root'
    )
    if passwd:
        kwargs['passwd'] = passwd

    conn = MySQLdb.connect(**kwargs)

    from thecodebase import CONFIG
    mysql_conf = CONFIG.get('mysql')
    if not mysql_conf:
        raise TypeError("Mysql configuration missing")
    
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % mysql_conf['db'])
    cursor.execute("GRANT ALL PRIVILEGES ON *.* TO '%s'@'localhost' IDENTIFIED BY '%s'" % (mysql_conf['user'], mysql_conf['passwd']))
    print("Mysql setup complete")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        root_passwd = None
    else:
        root_passwd = sys.argv[1]
    init_config()
    setup_mysql(root_passwd)
    init_database()
