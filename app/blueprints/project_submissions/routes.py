from app.blueprints.project_submissions import project_submissions_bp
from flask import render_template, request, session  # type: ignore
from flask_login import login_required, current_user  # type: ignore
from .services import (
    get_submitted_repos,
    fetch_public_repos,
    submit_repos_to_db,
    get_topics,
)
from app.extentions import cache


@project_submissions_bp.route("/submit", methods=["GET"])
@login_required
def submit():
    submitted_repos = get_submitted_repos(current_user.get_id())
    repos_final = get_topics(submitted_repos)
    return render_template("submit.html", user=current_user, repos=repos_final)


@project_submissions_bp.route("/projects/fetch_repos", methods=["POST"])
@login_required
def fetch_repos():
    cached_result = cache.get("fetched_repos")
    if cached_result:
        # log cached_result to file
        with open("cached_result.txt.tmp", "a") as f:
            f.write(str(cached_result) + "\n")
        return {"success": True, "repos": cached_result}
    user_id = current_user.get_id()
    repos = fetch_public_repos(user_id)
    cache.set("fetched_repos", repos, timeout=60)

    return {"success": True, "repos": repos}


@project_submissions_bp.route("/projects/submit_repos", methods=["POST"])
@login_required
def submit_repos():
    data = request.get_json()
    repositories = data.get("repositories")

    user_id = current_user.get_id()
    filtered_repositories = [
        repo for repo in session["fetched_repos"] if repo["name"] in repositories
    ]
    submit_repos_to_db(user_id, filtered_repositories)

    # Update the list of submitted projects
    submitted_repos = get_submitted_repos(user_id)
    # log submitted_repos to file
    with open("submitted_repos.txt.tmp", "a") as f:
        f.write(str(submitted_repos) + "\n")
    return render_template("submit.html", user=current_user, repos=submitted_repos)
