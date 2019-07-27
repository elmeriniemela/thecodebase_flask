
from flask import Blueprint

from .users import users
from .games import games
from .rest import rest
from .admin import admin
from .main import main
from .projects import projects

class NestableBlueprint(Blueprint):
    """
    Hacking in support for nesting blueprints, until hopefully https://github.com/mitsuhiko/flask/issues/593 will be resolved
    """

    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)
        self.record(deferred)


views = NestableBlueprint('views', __name__, template_folder='templates')

views.register_blueprint(users)
views.register_blueprint(games)
views.register_blueprint(rest)
views.register_blueprint(admin)
views.register_blueprint(main)
views.register_blueprint(projects)
