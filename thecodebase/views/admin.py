


from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint


from thecodebase.lib.wrappers import only_admins


from thecodebase.lib.actions import get_repos, delete_repos, update_repos


admin = Blueprint('admin', __name__, template_folder='templates')



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
