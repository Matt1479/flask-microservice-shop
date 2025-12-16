from flask import flash, redirect, session, url_for
from functools import wraps
from typing import Any
from urllib.parse import urlencode

import requests


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


def create_log(url: str, token: str, method: str | None, endpoint: str | None, *params):
    query_params = {}
    for arg in params:
        if isinstance(arg, dict):
            query_params.update(arg)

    query_string = urlencode(query_params)

    action = f"{method} /{endpoint}"
    if query_string:
        action += f"?{query_string}"

    response = requests.post(
        url,
        json={"action": action},
        cookies={"token": token}
    )

    if response.status_code != 200:
        flash("Could not create a log", category="error")
        return False
    
    return True
