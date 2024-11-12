from flask import Blueprint  # type: ignore

errors = Blueprint("errors", __name__, template_folder="templates")

from . import routes
