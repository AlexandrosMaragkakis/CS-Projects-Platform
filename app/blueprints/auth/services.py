from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
from .models import User, Student, Company
from flask import session  # type: ignore


def register_user(
    email, password, confirm_password, full_name, user_type, company_name=None
):
    if password != confirm_password:
        return False
    if User.get_by_email(email):
        return False
    hashed_password = generate_password_hash(password)

    if user_type == "student":
        username = email.split("@")[0]
        user = Student(
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            username=username,
        )
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
