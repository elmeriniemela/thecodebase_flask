
from datetime import datetime

from flask import request
from flask import session

from .dbconnect import Cursor

def update_repos(username, password):
    from github import Github
    import requests
    import markdown
    g = Github(username, password)

    repos = []
    for repo in g.get_user().get_repos():
        if not repo.private and repo.owner.login == username:
            try:
                readme = repo.get_readme()
            except:
                continue
            print(repo.name)
            readme_str = requests.get(readme.download_url).text
            readme_html = markdown.markdown(readme_str)
            repo.readme_html = readme_html
            repos.append(repo)

    with Cursor() as cur:
        cur.execute("SELECT name, repo_id, noupdate FROM Repo")
        existing = {t[0]: (t[1], t[2]) for t in cur.fetchall()}
    
        for repo in repos:
            if repo.name in existing:
                repo_id, noupdate = existing[repo.name]
                if not noupdate:
                    cur.execute("UPDATE Repo SET readme_html=%s, updated=%s WHERE repo_id=%s",
                        (repo.readme_html, datetime.now(), repo_id)
                    )
            else:
                cur.execute("INSERT INTO Repo (name, display_name, readme_html, updated) VALUES (%s, %s, %s, %s)",
                    (repo.name, repo.name, repo.readme_html, datetime.now(),)
                )


def delete_repos():
    with Cursor() as cur:
        cur.execute("DELETE FROM Repo")


def get_repos():
    with Cursor() as cur:
        cur.execute("SELECT * FROM Repo")
        columns = [col[0] for col in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    for row in rows:
        row['readme_html'] = row['readme_html'].decode()
    return rows


def save_endpoint(endpoint):

    data = {
        'time': str(datetime.now()),
        'remote_addr': request.environ.get('HTTP_X_REAL_IP', request.environ['REMOTE_ADDR']),
    }

    if endpoint:
        data.update({'endpoint': endpoint})

    if 'logged_in' in session and 'uid' in session:
        data.update({'uid': session['uid']})

    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('visits', columns, placeholders)

    with Cursor() as cur:
        cur.execute(sql, data.values())