
import logging

from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint


from thecodebase.lib.wrappers import only_admins
from thecodebase.lib import github_integration as github

logger = logging.getLogger(__name__)

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin/repos', methods=['GET'])
@only_admins
def admin_repos():
    repos = github.get_all_repos()
    return render_template(
        'admin.html',
        page_title='Github Repositories',
        repos=repos,
        enumerate=enumerate,
    )


@admin.route('/admin/repos/update-all', methods=['POST'])
@only_admins
def admin_update_all_repos():
    if request.method == 'POST':
        try:
            github.update_all_repos(
                username=request.form.get('username'),
                password=request.form.get('password')
            )
        except Exception as error:
            logger.exception(error)
            flash("Login failed.")
    return redirect(url_for('admin.admin_repos'))



@admin.route('/admin/repos/<int:repo_id>/update', methods=['POST'])
@only_admins
def admin_update_repo_by_id(repo_id):
    if request.method == 'POST':
        github.update_repo(repo_id, request.form)
    return redirect(url_for('admin.admin_repos'))

@admin.route('/admin/repos/delete-all', methods=['POST'])
@only_admins
def admin_delete_all_repos():
    if request.method == 'POST':
        github.delete_all_repos()
    return redirect(url_for('admin.admin_repos'))
