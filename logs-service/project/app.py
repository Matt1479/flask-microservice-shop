import os
from flask import Flask, jsonify, request
from typing import Any


app = Flask(__name__)
port = int(os.environ.get("PORT", 5003))

LOGS: list[dict[str, Any]] = []


@app.route("/api/logs", methods=["GET"])
def logs():
    return jsonify({"data": LOGS}), 200 if LOGS else 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
