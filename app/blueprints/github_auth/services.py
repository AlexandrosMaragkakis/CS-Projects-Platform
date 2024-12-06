from app.blueprints.auth.models import User


def update_github_username(user_id, github_username):
    user = User.get_by_id(user_id)
    user.github_username = github_username
    user.save()


def update_github_token(user_id, github_token):
    user = User.get_by_id(user_id)
    user.github_token = github_token
    user.save()
