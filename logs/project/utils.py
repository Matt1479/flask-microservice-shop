from flask import request


def validate_int(value):
    try:
        return int(value)
    except ValueError:
        return False


def require_user_id():
    user_id = request.headers.get("X-User-Id")

    if not user_id:
        raise Exception("user id is required", 401)

    return user_id


def require_admin_role():
    user_role = request.headers.get("X-User-Role")

    if not user_role:
        raise Exception("user role is required", 401)

    if user_role != "admin":
        raise Exception("You have insufficient rights to access this resource", 403)

    return user_role
