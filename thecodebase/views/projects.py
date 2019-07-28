


from flask import render_template
from flask import Blueprint


from thecodebase.lib.wrappers import login_required
from thecodebase import content


projects = Blueprint('projects', __name__, template_folder='templates')



def create_topic(topic):
    kwargs = dict(
        topic=topic,
        repos=content.repos[topic.url],
        projects=True,
        bg='programming_header.jpg',
        page_title='Projects'
    )
    projects.route('/{}/'.format(topic.url), endpoint=topic.url)(
        login_required(lambda: render_template('projects.html', **kwargs))
    )

for key in content.topics:
    create_topic(key)
