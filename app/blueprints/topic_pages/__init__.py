from flask import Blueprint  # type: ignore

topic_bp = Blueprint("topic", __name__, template_folder="templates")

from . import routes
