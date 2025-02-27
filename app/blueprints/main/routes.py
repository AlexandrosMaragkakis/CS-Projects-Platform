from flask import render_template  # type: ignore
from . import main_bp
from flask_login import login_required, current_user  # type: ignore


# Home Page
@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
