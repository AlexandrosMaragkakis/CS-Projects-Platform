from app.blueprints.auth.models import User
import requests  # type: ignore
from flask import redirect, url_for, jsonify, session  # type: ignore
from flask import current_app as app  # type: ignore
from flask_login import current_user  # type: ignore
import logging


def get_submitted_repos(user_id):
    return []


def fetch_public_repos(user_id):

    access_token = User.get_by_id(user_id).github_token
    # log
    logging.debug("Access token: %s", access_token)

    if not access_token:
        return {"success": False, "message": "No access token present"}

    username = current_user.github_username
    repos_info = []
    page = 1
    while True:
        repos_response = requests.get(
            f"{app.config['GITHUB_API_BASE_URL']}/users/{username}/repos?page={page}&per_page=100",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        if repos_response.status_code != 200:
            # log
            logging.error("Failed to get repos: %s", repos_response.status_code)
            return jsonify({"success": False, "message": "Failed to get repos."})

        repos = repos_response.json()
        repos_info.extend(repos)

        if len(repos) < 100:
            break
        page += 1

    filtered_repos = [
        {
            "name": repo["name"],
            "url": repo["html_url"],
            "description": repo["description"],
            "topics": repo.get("topics", []),
        }
        for repo in repos_info
    ]

    # log
    logging.info("Fetched %d repositories.", len(filtered_repos))
    session["fetched_repos"] = filtered_repos
    return filtered_repos
