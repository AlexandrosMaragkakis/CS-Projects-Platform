from flask_login import LoginManager
from neomodel import config as neomodel_config

# from authlib.integrations.flask_client import OAuth
from .blueprints.auth.models import User


def load_user(user_id):
    return User.get_by_id(user_id)


login_manager = LoginManager()
login_manager.user_loader(load_user)
# oauth = OAuth()


def init_extensions(app):

    login_manager.init_app(app)

    # oauth.init_app(app)
    # oauth.register(
    #    name="github",
    #    client_id=app.config["GITHUB_CLIENT_ID"],
    #    client_secret=app.config["GITHUB_CLIENT_SECRET"],
    #    authorize_url=app.config["GITHUB_AUTHORIZE_URL"],
    #    access_token_url=app.config["GITHUB_ACCESS_TOKEN_URL"],
    #    client_kwargs={"scope": "repo"},
    # )

    configure_neo4j(app)


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
