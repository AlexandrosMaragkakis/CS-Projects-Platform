from flask import Blueprint  # type: ignore

search_bp = Blueprint("search", __name__, template_folder="templates")

from . import routes
