from flask import request


def validate_int(value):
    try:
        return int(value)
    except ValueError:
        return False


def require_user_id():
    user_id = request.headers.get("X-User-Id")

    if not user_id:
        raise ValueError("user id is required")

    return user_id


def require_role():
    user_role = request.headers.get("X-User-Role")

    if not user_role:
        raise ValueError("user role is required")

    return user_role
