from flask import redirect, session, url_for
from functools import wraps
from typing import Any


def token_required(f):
    """Decorate routes to require token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("token"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """
    Decorate routes to require the role of admin.
    
    Make sure to decorate with token_required first.
    Reason: Decorators are applied bottom-to-top and executed top-to-bottom.
    Example:
        @app.route("/protected-route")
        @token_required
        @admin_required
        def protected_route():
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        user: dict[str, Any] | None = session.get("user")

        if user:
            if user.get("role") != "admin":
                return redirect(url_for("index"))
        
        return f(*args, **kwargs)
    
    return decorated
