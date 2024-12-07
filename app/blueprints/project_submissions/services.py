import requests  # type: ignore
from flask import redirect, url_for, jsonify, session  # type: ignore
from flask import current_app as app  # type: ignore
from flask_login import current_user  # type: ignore
from app.models.project import Project
from app.models.user import Student
from app.models.topic import Topic


def get_submitted_repos(user_id):
    user = Student.get_by_id(user_id)
    return user.worked_in.all()


def get_topics(projects):
    for project in projects:
        topics = project.tagged_with.all()
        project.topics = [topic.name for topic in topics]

    return projects


def submit_repos_to_db(user_id, repositories):
    try:
        for repo in repositories:

            submitted_repos = get_submitted_repos(user_id)

            if repo["url"] in [project.github_url for project in submitted_repos]:
                continue

            # Create a new project
            project = Project(
                github_id=repo["github_id"],
                title=repo["name"],
                github_url=repo["url"],
                description=repo["description"],
            )
            project.save()

            # Connect the project to the user
            user = Student.get_by_id(user_id)
            user.worked_in.connect(project)
            user.save()

            # Connect the project to the topics
            for topic_name in repo["topics"]:
                topic = Topic.nodes.get_or_none(name=topic_name)

                if topic is None:
                    topic = Topic(name=topic_name)
                    topic.save()

                project.tagged_with.connect(topic)
                user.skilled_in.connect(topic)

                project.save()
            user.save()

    except Exception as e:
        raise e


def fetch_public_repos(user_id):
    from app.models.user import User

    access_token = User.get_by_id(user_id).github_token

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
            return jsonify({"success": False, "message": "Failed to get repos."})

        repos = repos_response.json()
        repos_info.extend(repos)

        if len(repos) < 100:
            break
        page += 1
    # log response to file
    # with open("repos_response.txt.tmp", "w") as f:
    #    f.write(str(repos_response.json()))
    filtered_repos = [
        {
            "github_id": repo["id"],
            "name": repo["name"],
            "url": repo["html_url"],
            "description": repo["description"],
            "topics": repo.get("topics", []),
        }
        for repo in repos_info
    ]

    session["fetched_repos"] = filtered_repos
    # log filtered_repos to file with all contents
    with open("filtered_repos.txt.tmp", "w") as f:
        f.write(str(filtered_repos))
    return filtered_repos


def delete_project(github_id):
    project = Project.nodes.get_or_none(github_id=github_id)
    if project is None:
        raise ValueError(f"Project with github_id {github_id} not found")

    topics = project.tagged_with.all()
    project.delete()

    for topic in topics:
        topic.delete_if_orphan()
