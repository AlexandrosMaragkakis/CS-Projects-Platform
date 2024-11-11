from flask import jsonify, request, url_for, redirect, session  # type: ignore
from flask_login import login_user, logout_user, current_user  # type: ignore

# from .models import User
from app.blueprints.auth import auth_bp
from .services import authenticate_user, register_user


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = authenticate_user(email, password)
    if user is not None:
        login_user(user)
        if user.github_token is not None and user.github_username is not None:
            session["github_authenticated"] = True
        else:
            session["github_authenticated"] = False
        # write session to file
        with open("session.txt.tmp", "w") as f:
            f.write(str(session))
        return jsonify({"success": True, "redirect_url": url_for("main.profile")})
    else:
        return jsonify({"success": False, "message": "Invalid email or password."})


@auth_bp.route("/register_student", methods=["POST"])
def register_student():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    full_name = data.get("full_name")

    user = register_user(
        email=email,
        password=password,
        confirm_password=confirm_password,
        full_name=full_name,
        user_type="student",
    )
    if user:
        login_user(user)
        if user.github_token is not None and user.github_username is not None:
            session["github_authenticated"] = True
        else:
            session["github_authenticated"] = False
        return jsonify({"success": True, "redirect_url": url_for("main.profile")})
    else:
        return jsonify({"success": False, "message": "Something went wrong."})


@auth_bp.route("/register_company", methods=["POST"])
def register_company():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    full_name = data.get("full_name")
    company_name = data.get("company_name")

    user = register_user(
        email=email,
        password=password,
        confirm_password=confirm_password,
        full_name=full_name,
        user_type="company",
        company_name=company_name,
    )
    if user:
        return redirect(url_for("main.home", next="login_required"))
    else:
        return jsonify({"success": False, "message": "Something went wrong."})


@auth_bp.route("/logout")
def logout():
    session.clear()
    logout_user()
    session.clear()
    return redirect(url_for("main.home"))


"""
@auth_bp.route("/github/connect")
def github_connect():
    #Redirects the user to GitHub for OAuth authorization
    github = oauth.create_client("github")
    redirect_uri = url_for("auth.github_callback", _external=True)
    return github.authorize_redirect(redirect_uri)


@auth_bp.route("/github/callback")
def github_callback():
    #Handles the callback from GitHub after authorization
    github = oauth.create_client("github")
    token = github.authorize_access_token()

    if not token:
        return (
            jsonify({"success": False, "message": "Failed to get access token."}),
            400,
        )

    # Store the access token in the session or the database
    session["github_token"] = token

    return redirect(url_for("submit"))


##### end github #####

"""


"""
@auth_bp.route("/github_auth", methods=["GET"])
@login_required
def github_auth():
    github_auth_url = f"{GITHUB_AUTH_URL}?client_id={GITHUB_CLIENT_ID}&scope=repo& \
        "redirect_uri={url_for('callback', _external=True)}"
    return redirect(github_auth_url)


@auth_bp.route("/callback", methods=["GET"])
@login_required
def callback():
    code = request.args.get("code")
    if code is None:
        return jsonify({"success": False, "message": "No code provided."}), 400

    # Exchange the authorization code for an access token
    response = requests.post(
        GITHUB_TOKEN_URL,
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
        headers={"Accept": "application/json"},
    )

    if response.status_code != 200:
        return (
            jsonify({"success": False, "message": "Failed to get access token."}),
            400,
        )

    # Parse the access token from the response
    access_token = response.json().get("access_token")
    if not access_token:
        return (
            jsonify({"success": False, "message": "Failed to get access token."}),
            400,
        )

    # Store the access token in the session
    session["access_token"] = access_token

    # Redirect to the submit page after successful authentication
    return redirect(url_for("submit"))

    """
