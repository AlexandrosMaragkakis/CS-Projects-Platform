from app.blueprints.search import search_bp
from flask import render_template, request, session  # type: ignore
from flask_login import login_required, current_user  # type: ignore
from .services import (
    search_by_topic_,
    get_available_topics,
    find_topics,
    find_users,
    find_projects,
)


@search_bp.route("/search", methods=["GET"])
@login_required
def search():
    return render_template("search.html")


@search_bp.route("/search/topics/<search_query>", methods=["GET"])
@login_required
def search_for_topics(search_query):

    try:
        matched_topics = find_topics(search_query)
        if matched_topics is None:
            return {"success": False, "error": "No matching topics"}
        return {"success": True, "topics": matched_topics}
    except Exception as e:
        return {"success": False, "error": str(e)}


@search_bp.route("/search/users", methods=["GET"])
@login_required
def search_for_users():
    query = request.args.get("query")
    if not query:
        return {"success": False, "error": "Query is required"}

    try:

        users = find_users(query)
        if users is None:
            return {"success": False, "error": "No matching users"}
        return {"success": True, "users": users}
    except Exception as e:
        return {"success": False, "error": str(e)}


@search_bp.route("/search/projects", methods=["GET"])
@login_required
def search_for_projects():
    query = request.args.get("query")
    if not query:
        return {"success": False, "error": "Query is required"}

    try:

        projects = find_projects(query)
        if projects is None:
            return {"success": False, "error": "No matching projects"}

        return {"success": True, "projects": projects}
    except Exception as e:
        return {"success": False, "error": str(e)}
