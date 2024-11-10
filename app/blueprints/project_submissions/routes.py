from app.blueprints.project_submissions import project_submissions_bp
from flask import render_template, session  # type: ignore
from flask_login import login_required, current_user  # type: ignore
from .services import get_submitted_repos


@project_submissions_bp.route("/submit", methods=["GET"])
@login_required
def submit():
    submitted_repos = get_submitted_repos(current_user.get_id())
    return render_template("submit.html", user=current_user, repos=submitted_repos)
