from flask import jsonify, request, url_for, redirect, session  # type: ignore
from flask_login import login_user, logout_user  # type: ignore

from app.blueprints.auth import auth_bp
from .services import authenticate_user, register_user
from .exceptions import UserAlreadyExistsError, InvalidCredentialsError


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = authenticate_user(email, password)
        login_user(user)

        if user.is_student:
            session["github_authenticated"] = bool(
                user.github_token is not None and user.github_username is not None
            )

        return jsonify({"success": True, "redirect_url": url_for("main.profile")})

    except InvalidCredentialsError as e:
        return jsonify({"success": False, "message": str(e)})


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    try:
        user = register_user(**data)
    except UserAlreadyExistsError as e:
        return jsonify({"success": False, "message": str(e)})

    login_user(user)
    return jsonify({"success": True, "redirect_url": url_for("main.profile")})


@auth_bp.route("/logout")
def logout():
    # probably had a reason to clear it twice
    # need to revisit
    session.clear()
    logout_user()
    session.clear()
    return redirect(url_for("main.home"))
