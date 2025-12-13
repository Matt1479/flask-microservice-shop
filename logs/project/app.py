import os
import utils
from datetime import datetime
from flask import Flask, jsonify, request
from typing import Any


app = Flask(__name__)
port = int(os.environ.get("PORT", 5003))

LOGS: list[dict[str, Any]] = []


@app.route("/api/logs", methods=["GET", "POST"])
def logs():
    try:
        user_id = utils.require_user_id()
        utils.require_admin_role()
    except Exception as e:
        return jsonify({"error": e.args[0]}), e.args[1]

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        
        if not data.get("action"):
            return jsonify({"error": "Missing required field: 'action'"}), 400
        
        data["id"] = max([log["id"] for log in LOGS]) + 1 if LOGS else 1
        data["timestamp"] = datetime.now()
        data["user_id"] = int(user_id)
        LOGS.append(data)
        return jsonify({"message": "Log added successfully"}), 200
    else:
        # GET
        return jsonify({"data": LOGS}), 200 if LOGS else 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
