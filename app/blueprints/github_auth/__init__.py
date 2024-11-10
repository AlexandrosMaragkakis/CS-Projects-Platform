from flask import Blueprint  # type: ignore

github_bp = Blueprint("github", __name__, template_folder="templates")
from . import routes
