# app/__init__.py

# imports
from flask import Flask  # type: ignore
from .config import config_by_name
from .extentions import init_extensions
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .blueprints.project_submissions import project_submissions_bp
from .blueprints.github_auth import github_bp
from .blueprints.error_hadling import errors
from .blueprints.search import search_bp
from .blueprints.user_pages import user_bp
from .blueprints.topic_pages import topic_bp


def create_app(config_name=None):
    """Factory function for creating the app object"""

    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_by_name[config_name or "development"])
    print(app.config)
    init_extensions(app)
    register_blueprints(app)

    return app


def register_blueprints(app):
    """Register all blueprints for the application"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_submissions_bp)
    app.register_blueprint(github_bp)
    app.register_blueprint(errors)
    app.register_blueprint(search_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(topic_bp)
