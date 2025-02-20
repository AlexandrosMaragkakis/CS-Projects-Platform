from flask import jsonify, url_for, redirect, session  # type: ignore
from flask_login import login_required, current_user  # type: ignore
from neomodel.exceptions import UniqueProperty  # type: ignore

from app.blueprints.github_auth import github_bp
from app.extensions import oauth
from .services import update_github_username, update_github_token


@github_bp.route("/github/connect", methods=["GET"])
@login_required
def github_connect():
    # Redirects the user to GitHub for OAuth authorization
    github = oauth.create_client("github")
    redirect_uri = url_for("github.github_callback", _external=True)
    return github.authorize_redirect(redirect_uri)


@github_bp.route("/github/callback")
@login_required
def github_callback():
    github = oauth.create_client("github")
    token = github.authorize_access_token()
    session["access_token"] = token
    if not token:
        return (
            jsonify({"success": False, "message": "Failed to get access token."}),
            400,
        )

    try:
        github_user_data = github.get("user").json()
        github_username = github_user_data["login"]

        update_github_username(current_user.get_id(), github_username)
        update_github_token(current_user.get_id(), token["access_token"])

        session["github_authenticated"] = True
        return redirect(url_for("project_submissions.submit"))

    except UniqueProperty:
        error_message = "GitHub account already exists."
        return redirect(url_for("project_submissions.submit", error=error_message))
