from flask import Blueprint  # type: ignore

user_bp = Blueprint("user", __name__, template_folder="templates")

from . import routes
