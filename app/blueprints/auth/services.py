from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
from app.models.user import User, Student, Company
from neomodel.exceptions import UniqueProperty  # type: ignore
from .exceptions import UserAlreadyExistsError, InvalidCredentialsError


def register_user(user_type, **data):

    hashed_password = generate_password_hash(data["password"])

    if user_type == "student":
        user = Student(
            email=data["email"],
            password_hash=hashed_password,
            full_name=data["full_name"],
        )
    elif user_type == "company":
        user = Company(
            email=data["email"],
            password_hash=hashed_password,
            full_name=data.get("full_name"),
            company_name=data["company_name"],
        )
    else:
        raise ValueError("Invalid user type")

    try:
        user.save()
    except UniqueProperty:
        raise UserAlreadyExistsError("User already exists")
    return user


def authenticate_user(email, password):
    user = User.get_by_email(email)
    if not user:
        raise InvalidCredentialsError("Invalid email or password")

    if not check_password_hash(user.password_hash, password):
        raise InvalidCredentialsError("Invalid email or password")

    return user
