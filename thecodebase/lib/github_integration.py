


import logging
from datetime import datetime


import requests
from github import Github
import markdown

from .dbconnect import Cursor
from . import sql


logger = logging.getLogger(__name__)

def update_all_repos(username, password):
    g = Github(username, password)
    repos = []
    for repo in g.get_user().get_repos():
        if not repo.private and repo.owner.login == username:
            try:
                readme = repo.get_readme()
            except:
                continue
            logger.info("Updated repo %s", repo.name)
            readme_str = requests.get(readme.download_url).text
            readme_html = markdown.markdown(readme_str)
            repo.readme_html = readme_html
            repos.append(repo)

    with Cursor() as cur:
        cur.execute("SELECT name, repo_id, noupdate FROM Repo")
        existing = {t[0]: (t[1], t[2]) for t in cur.fetchall()}
    
        for repo in repos:
            row = {
                'readme_html': repo.readme_html,
                'updated': datetime.now(),
            }
            if repo.name in existing:
                repo_id, noupdate = existing[repo.name]
                if not noupdate:
                    sql.update_row('Repo', row, repo_id=repo_id)
            else:
                row.update(display_name=repo.name, name=repo.name)
                sql.insert_row('Repo', row)
                


def delete_all_repos():
    with Cursor() as cur:
        cur.execute("DELETE FROM Repo")


def get_all_repos():
    with Cursor() as cur:
        cur.execute("SELECT * FROM Repo")
        columns = [col[0] for col in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    for row in rows:
        row['readme_html'] = row['readme_html'].decode()
    return rows

def update_repo(repo_id, vals):
    data = {
        'display_name': vals['display_name'],
        'readme_html': vals['readme_html'],
        'noupdate': bool(vals.get('noupdate', False)),
        'updated': datetime.now()
    }

    sql.update_row('Repo', data, repo_id=repo_id)