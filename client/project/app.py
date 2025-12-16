import os
from typing import Any
import requests
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from utils import admin_required, token_required


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
BASE_API_URL = f"http://localhost:{port}/api"
API_ENDPOINTS = {
    "auth": BASE_API_URL + "/auth",
    "logs": BASE_API_URL + "/logs",
    "shop": BASE_API_URL + "/shop"
}

# Store sessions on disk
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24)
Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Clear session (token, user)
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("must provide username", "error")
            return redirect(url_for("login"))
        
        if not password:
            flash("must provide password", "error")
            return redirect(url_for("login"))
        
        # Make a POST request to /auth/login
        response = requests.post(
            f"{API_ENDPOINTS["auth"]}/login",
            json={"username": username, "password": password}
        )
        data: dict[str, Any] = response.json()

        # If an error occurred (invalid username/password, etc.)
        if data.get("error"):
            flash(str(data.get("error")), category="error")
            return redirect(url_for("login"))

        # Store token in session
        session["token"] = response.cookies.get("token")
        if not session.get("token"):
            flash("Could not get token", category="error")
            return redirect(url_for("login"))
        
        # Store user in session
        session["user"] = {
            "id": data["user_id"],
            "role": data["user_role"]
        }
        if not session.get("user"):
            flash("Could not get user", category="error")
            return redirect(url_for("login"))

        # Redirect to index
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    if session.get("token"):
        # Send a DELETE request to /auth/logout
        requests.delete(
            f"{API_ENDPOINTS["auth"]}/logout",
            cookies={"token": session["token"]}
        )

    # Clear session (token, user)
    session.clear()
    
    return redirect(url_for("login"))


@app.route("/logs")
@token_required
@admin_required
def logs():
    """Display logs"""
    try:
        response_json = requests.get(
            f"{API_ENDPOINTS['logs']}",
            # Index into session directly thanks to token_required
            cookies={"token": session["token"]}
        ).json()
        data: list[dict[str, Any]] = response_json.get("data")
    except requests.exceptions.JSONDecodeError:
        data = []

    return render_template("logs.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
