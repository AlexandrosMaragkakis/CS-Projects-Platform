from flask import jsonify, request, url_for, redirect, session  # type: ignore
from flask_login import login_user, logout_user, current_user  # type: ignore

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

        # session["github_authenticated"] = bool(getattr(user, "github_token", None) and getattr(user, "github_username", None))

        if user.github_token is not None and user.github_username is not None:
            session["github_authenticated"] = True
        else:
            session["github_authenticated"] = False

        # write session to file
        # with open("session.txt.tmp", "w") as f:
        #    f.write(str(session))
        return jsonify({"success": True, "redirect_url": url_for("main.profile")})

    except InvalidCredentialsError as e:
        return jsonify({"success": False, "message": str(e)})


@auth_bp.route("/register_student", methods=["POST"])
def register_student():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    try:
        user = register_user(
            email=email,
            password=password,
            full_name=full_name,
            user_type="student",
        )
    except UserAlreadyExistsError as e:
        return jsonify({"success": False, "message": str(e)})

    login_user(user)
    if user.github_token is not None and user.github_username is not None:
        session["github_authenticated"] = True
    else:
        session["github_authenticated"] = False
    return jsonify({"success": True, "redirect_url": url_for("main.profile")})


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
