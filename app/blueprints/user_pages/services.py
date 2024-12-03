from app.blueprints.auth.models import User


def get_user_info(username):
    user = User.get_by_username(username)

    if user is None:
        return None

    user_info = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "github_url": "https://github.com/" + user.github_username,
    }

    return user_info


def get_submitted_repos(user_id):
    user = User.get_by_id(user_id)
    return user.worked_in.all()


def get_topics(projects):
    for project in projects:
        topics = project.tagged_with.all()
        project.topics = [topic.name for topic in topics]

    return projects
