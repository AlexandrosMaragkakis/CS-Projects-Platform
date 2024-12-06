from app.blueprints.user_pages import user_bp
from flask import render_template  # type: ignore

from flask_login import login_required, current_user  # type: ignore
from .services import get_user_info, get_submitted_repos, get_topics


@user_bp.route("/users/<user_id>", methods=["GET"])
@login_required
def users(user_id):
    """Public user page"""

    user_info = get_user_info(user_id)
    submitted_repos = get_submitted_repos(current_user.get_id())
    projects = get_topics(submitted_repos)
    topics = sorted(
        {topic for project in projects for topic in project.topics}, key=str.lower
    )

    return render_template(
        "user.html", user_info=user_info, projects=projects, topics=topics
    )
