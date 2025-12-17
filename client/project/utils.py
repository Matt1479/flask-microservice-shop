from flask import flash, redirect, session, url_for
from functools import wraps
from typing import Any

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


def create_log(url: str, token: str, method: str, endpoint: str | None, params: list=[]):
    payload = {}
    for param in params:
        if isinstance(param, dict):
            payload.update(param)

    response = requests.post(
        url,
        json={
            "method": method,
            "endpoint": endpoint,
            "payload": payload
        },
        cookies={"token": token}
    )

    if response.status_code != 200:
        flash(
            f"Could not create a log (reason: {response.json().get('error')})",
            category="error",
        )
        return False
    
    return True
