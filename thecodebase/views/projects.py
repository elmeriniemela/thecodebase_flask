


from flask import render_template
from flask import Blueprint


from thecodebase.lib.wrappers import login_required
from thecodebase.lib.github_integration import get_all_repos
from thecodebase.content import Projects

TOPIC_DICT = Projects()


projects = Blueprint('projects', __name__, template_folder='templates')



@projects.route('/github-projects/')
@login_required
def github_projects():
    kwargs = dict(
        repos=get_all_repos(),
        projects=True,
        bg='programming_header.jpg',
        page_title='Github Projects'
    )
    return render_template("github.html", **kwargs)


def create_topic(topic):
    kwargs = dict(
        topic=topic,
        projects=True,
        bg='programming_header.jpg',
        page_title='Projects'
    )
    projects.route('/{}/'.format(topic.url), endpoint=topic.url)(
        login_required(lambda: render_template('projects.html', **kwargs))
    )

for key in TOPIC_DICT:
    create_topic(key)