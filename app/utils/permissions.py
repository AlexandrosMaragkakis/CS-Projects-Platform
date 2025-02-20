from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
from neomodel import StructuredNode


def role_required(allowed_roles: list[StructuredNode]):
    def wrapper(fn):
        @wraps(fn)
        def wrapper_role_required(*args, **kwargs):
            # Get the actual user object from the proxy
            user_obj = current_user._get_current_object()
            if not isinstance(user_obj, tuple(allowed_roles)):

                return redirect(url_for("main.home", next="permissions_error"))
            return fn(*args, **kwargs)

        return wrapper_role_required

    return wrapper
