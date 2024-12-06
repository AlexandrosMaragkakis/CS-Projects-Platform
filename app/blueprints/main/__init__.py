from flask import Blueprint  # type: ignore

main_bp = Blueprint("main", __name__, template_folder="templates")

from . import routes
