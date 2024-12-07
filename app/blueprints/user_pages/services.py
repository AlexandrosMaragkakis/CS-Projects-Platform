from app.models.user import User


def get_user_info(user_id):
    user = User.get_by_id(user_id)

    if user is None:
        return None

    github_url = None
    if user.github_username is not None:
        github_url = "https://github.com/" + user.github_username

    user_info = {
        "full_name": user.full_name,
        "email": user.email,
        "github_url": github_url,
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
