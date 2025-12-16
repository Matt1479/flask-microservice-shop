import os
from typing import Any
import requests
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session


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
Session(app)

client = requests.Session()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Clear all cookies (including token)
    client.cookies.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("must provide username", "error")
            return redirect(url_for("login"))
        
        if not password:
            flash("must provide password", "error")
            return redirect(url_for("login"))
        
        # Make a POST request to auth service: /login
        response = client.post(
            f"{API_ENDPOINTS["auth"]}/login",
            json={"username": username, "password": password}
        )
        response_json: dict[str, Any] = response.json()

        # If an error occurred (invalid username/password, etc.)
        if response_json.get("error"):
            flash(str(response_json.get("error")), category="error")
            return redirect(url_for("login"))

        token = response.cookies.get("token")

        if not token:
            flash("Could not get token", category="error")
            return redirect(url_for("login"))
        
        # Set a cookie: token
        client.cookies.set("token", token)

        # Redirect to index
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    client.delete(f"{API_ENDPOINTS["auth"]}/logout")

    # Clear all cookies (including token)
    client.cookies.clear()
    
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
