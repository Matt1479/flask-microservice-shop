import requests
from flask import Flask, jsonify, request, make_response
import json
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

port = int(os.environ.get("PORT", 5001))

with open("./project/users.json", "r") as f:
    users = json.load(f)


@app.route("/api/")
def index():
    return "Hello, this is Auth Service"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
