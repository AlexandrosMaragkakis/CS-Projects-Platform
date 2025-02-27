from flask import Blueprint  # type: ignore

job_posting_bp = Blueprint("job_posting", __name__, template_folder="templates")

from . import routes
