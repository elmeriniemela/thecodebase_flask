

from datetime import datetime


from flask import Response
from flask import session
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint


from thecodebase import Cursor
from thecodebase.wrappers import only_admins


admin = Blueprint('admin', __name__, template_folder='templates')

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


@admin.route('/admin/repos', methods=['GET'])
@only_admins
def admin_repos():
    return render_template(
        'admin.html',
        page_title='Admin View',
        repos=get_repos(),
        enumerate=enumerate,
    )

@admin.route('/admin/repos/update-all', methods=['POST'])
@only_admins
def admin_update_all_repos():
    if request.method == 'POST':
        try:
            update_repos(request.form.get('username'), request.form.get('password'))
        except:
            flash("Login failed.")
    return redirect(url_for('admin.admin_repos'))

@admin.route('/admin/repos/delete-all', methods=['POST'])
@only_admins
def admin_delete_all_repos():
    if request.method == 'POST':
        delete_repos()
    return redirect(url_for('admin.admin_repos'))
