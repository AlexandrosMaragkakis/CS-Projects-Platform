from flask import Blueprint  # type: ignore

project_submissions_bp = Blueprint(
    "project_submissions", __name__, template_folder="templates"
)

from . import routes
