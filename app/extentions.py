from flask_login import LoginManager  # type: ignore
from neomodel import config as neomodel_config  # type: ignore
from flask_caching import Cache  # type: ignore

from authlib.integrations.flask_client import OAuth  # type: ignore
from .blueprints.auth.models import User

from flask import request, jsonify, redirect, url_for  # type: ignore


login_manager = LoginManager()
cache = Cache(config={"CACHE_TYPE": "simple"})


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():

    return redirect(url_for("main.home", next="login_required"))


# login_manager.user_loader(load_user)
oauth = OAuth()


def init_extensions(app):

    login_manager.init_app(app)

    oauth.init_app(app)
    oauth.register(
        name="github",
        client_id=app.config["GITHUB_CLIENT_ID"],
        client_secret=app.config["GITHUB_CLIENT_SECRET"],
        authorize_url=app.config["GITHUB_AUTHORIZE_URL"],
        access_token_url=app.config["GITHUB_ACCESS_TOKEN_URL"],
        access_token_params=None,
        base_url=app.config["GITHUB_API_BASE_URL"],
        authorize_params=None,
        client_kwargs={"scope": "repo"},
    )

    configure_neo4j(app)

    cache.init_app(app)


def configure_neo4j(app):
    """
    Set up Neo4j database connection parameters.
    """
    neomodel_config.DATABASE_URL = (
        "bolt://"
        + app.config["NEO4J_USERNAME"]
        + ":"
        + app.config["NEO4J_PASSWORD"]
        + "@"
        + app.config["NEO4J_URI"]
    )
