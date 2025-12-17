import os
import utils

from datetime import datetime
from flask import Flask, jsonify, request
from typing import Any
from urllib.parse import urlencode


app = Flask(__name__)
port = int(os.environ.get("PORT", 5003))

REQUIRED_FIELDS = ["method", "endpoint"]
OPTIONAL_FIELD = "payload"

LOGS: list[dict[str, Any]] = []


@app.route("/api/logs", methods=["GET", "POST"])
def logs():
    try:
        user_id = utils.require_user_id()
        user_role = utils.require_role()
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    if request.method == "POST":
        data: dict[str, Any] | Any | None = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        
        log = {
            "id": max([log["id"] for log in LOGS]) + 1 if LOGS else 1,
            "timestamp": datetime.now(),
            "user_id": int(user_id),
            "user_role": user_role
        }

        for field in REQUIRED_FIELDS:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
            log[field] = data[field]

        if OPTIONAL_FIELD in data:
            try:
                log[OPTIONAL_FIELD] = urlencode(data[OPTIONAL_FIELD])
            except TypeError as e:
                return jsonify({"error": str(e)}), 400

        LOGS.append(log)

        return jsonify({"message": "Log added successfully"}), 200
    else:
        # GET
        return jsonify({"data": LOGS}), 200 if LOGS else 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
