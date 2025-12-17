from flask import Flask, jsonify, request, make_response
import jwt
import json
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

port = int(os.environ.get("PORT", 5001))

with open("./project/users.json", "r") as f:
    users = json.load(f)


@app.route("/api/auth")
def index():
    return jsonify({"message": "Hello, this is Auth Service"})


@app.route("/api/auth/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type"}), 415
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    username = data.get("username")
    password = data.get("password")
    for user in users:
        if user["username"] == username and user["password"] == password:
            token = jwt.encode(
                {"user_id": user["id"], "user_role": user["role"]},
                app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            response = make_response(jsonify({
                "message": "Authentication successful",
                "user_id": user["id"],
                "user_role": user["role"]
            }))
            response.set_cookie("token", token)
            return response, 200
    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/api/auth/logout", methods=["DELETE"])
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    response.delete_cookie("token")
    return response, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
