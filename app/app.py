from flask import Flask, jsonify, render_template, request, url_for, redirect, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY


app = Flask(__name__, static_url_path="/static")
app.config["SECRET_KEY"] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


users = {}


class User(UserMixin):
    def __init__(self, user_id, email, role, full_name, password):
        self.id = user_id
        self.email = email
        self.role = role
        self.full_name = full_name
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user


# Home Page
@app.route("/")
def home():

    return render_template("index.html")


@login_manager.unauthorized_handler
def unauthorized():
    # Check if the request is an AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return (
            jsonify(
                {"success": False, "message": "Please log in to access this page."}
            ),
            401,
        )
    else:
        return redirect(url_for("home", next="login_required"))


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email in users:
        user = users[email]
        if check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"success": True, "redirect_url": url_for("profile")})
    else:
        return jsonify({"success": False, "message": "Invalid email or password."})


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("home"))


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    full_name = data.get("full_name")
    role = "student"

    if email in users:
        return jsonify({"success": False, "message": "User already exists."})

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match."})

    hashed_password = generate_password_hash(password)
    user = User(len(users) + 1, email, role, full_name, hashed_password)
    users[email] = user

    login_user(user)
    return jsonify({"success": True, "redirect_url": url_for("profile")})


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
