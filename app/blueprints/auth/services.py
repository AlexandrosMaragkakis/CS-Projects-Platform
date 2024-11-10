from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Student, Company


def register_user(
    email, password, confirm_password, full_name, user_type, company_name=None
):
    if password != confirm_password:
        return False
    if User.get_by_email(email):
        return False
    hashed_password = generate_password_hash(password)

    if user_type == "student":
        user = Student(email=email, password_hash=hashed_password, full_name=full_name)
    elif user_type == "company":
        user = Company(
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            company_name=company_name,
        )
    else:
        raise ValueError("Invalid user type")

    user.save()
    return user


def authenticate_user(email, password):
    user = User.get_by_email(email)
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


"""
def github_oauth():
    # Redirect to GitHub for authentication
    github = oauth.create_client("github")
    redirect_uri = url_for("auth.github_callback", _external=True)
    return github.authorize_redirect(redirect_uri)


def github_oauth_callback():
    # Handle GitHub OAuth callback and retrieve user information
    github = oauth.create_client("github")
    token = github.authorize_access_token()
    github_user = github.get("user").json()

    # Find or create a user with the GitHub information
    username = github_user["login"]
    user = User.get_by_username(username)
    if not user:
        user = User(username=username)
        user.save()
    return user
"""
