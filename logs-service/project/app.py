import os
from datetime import datetime
from flask import Flask, jsonify, request
from project import utils
from typing import Any


app = Flask(__name__)
port = int(os.environ.get("PORT", 5003))

LOGS: list[dict[str, Any]] = []


@app.route("/api/logs", methods=["GET", "POST"])
def logs():
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        
        if not data.get("user_id") or not data.get("action"):
            return jsonify({"error": "Missing required field(s)"}), 400
        
        if not utils.validate_int(data.get("user_id")):
            return jsonify({"error": "user_id must be an integer."}), 400
        
        data["id"] = max([log["id"] for log in LOGS]) + 1 if LOGS else 1
        data["timestamp"] = datetime.now()
        LOGS.append(data)
        return jsonify({"message": "Log added successfully"}), 200
    else:
        # GET
        return jsonify({"data": LOGS}), 200 if LOGS else 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
