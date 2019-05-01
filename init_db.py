def init_database():
    from thecodebase.dbconnect import Cursor
    tables = {
        'users': """
            CREATE TABLE users (
                uid INT(11) AUTO_INCREMENT PRIMARY KEY, 
                username VARCHAR(20), 
                password VARCHAR(100), 
                email VARCHAR(50), 
                settings VARCHAR(32500), 
                tracking VARCHAR(32500), 
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

    test_sql = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'thecodebase'
    AND table_name = %s;
    """
    created = []
    for table, query in tables.items():
        with Cursor() as cur:
            table_exists = cur.execute(test_sql, (table, ))
            if not table_exists:
                cur.execute(query)
                created.append(table)
    if created:
        print("Created new tables: {}".format(', '.join(created)))
    else:
        print("No new tables created")

init_database()
