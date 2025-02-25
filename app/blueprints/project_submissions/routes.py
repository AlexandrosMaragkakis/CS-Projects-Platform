from app.blueprints.project_submissions import project_submissions_bp
from flask import render_template, request, session  # type: ignore
from flask_login import login_required, current_user  # type: ignore
from .services import (
    get_submitted_repos,
    fetch_public_repos,
    submit_repos_to_db,
    get_topics,
    delete_project,
)
from app.extensions import cache
from app.models.user import Student
from app.utils.permissions import role_required


@project_submissions_bp.route("/submit", methods=["GET"])
@login_required
@role_required(allowed_roles=[Student])
def submit():
    submitted_repos = get_submitted_repos(current_user.get_id())
    repos_final = get_topics(submitted_repos)
    return render_template("submit.html", user=current_user, repos=repos_final)


@project_submissions_bp.route("/projects/fetch_repos", methods=["POST"])
@login_required
@role_required(allowed_roles=[Student])
def fetch_repos():
    user_id = current_user.get_id()
    cached_result = cache.get(f"fetched_repos_{user_id}")
    if cached_result:
        # log cached_result to file, probably useful for metrics
        with open("cached_result.txt.tmp", "a") as f:
            f.write(str(cached_result) + "\n")
        return {"success": True, "repos": cached_result}

    repos = fetch_public_repos(user_id)
    cache.set(f"fetched_repos_{user_id}", repos, timeout=60)

    return {"success": True, "repos": repos}


@project_submissions_bp.route("/projects/submit_repos", methods=["POST"])
@login_required
@role_required(allowed_roles=[Student])
def submit_repos():
    data = request.get_json()
    repositories = data.get("repositories")

    user_id = current_user.get_id()
    filtered_repositories = [
        repo for repo in session["fetched_repos"] if repo["name"] in repositories
    ]
    try:
        submit_repos_to_db(user_id, filtered_repositories)
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": True}


@project_submissions_bp.route("/projects/delete/<int:github_id>", methods=["POST"])
@login_required
@role_required(allowed_roles=[Student])
def delete(github_id):
    try:
        delete_project(github_id)

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
