import jwt
import os
import requests
from flask import Flask, jsonify, make_response, request


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
port = int(os.environ.get("PORT", 5000))

SERVICE_ROUTES = {
    "/api/auth": "http://localhost:5001",
    "/api/shop": "http://localhost:5002",
    "/api/logs": "http://localhost:5003"
}


@app.before_request
def check_auth():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Authorization token is missing"}), 401
    
    try:
        data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        user_id = data["user_id"]
    except jwt.exceptions.DecodeError:
        return jsonify({"error": "Authorization token is invalid"}), 401


@app.route("/")
def index():
    return jsonify({"message": "Hello, this is API gate"}), 200


@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def gateway(path: str):
    incoming_path = "/" + str(path)

    # Find matching service
    service_url = None
    for route_prefix, backend in SERVICE_ROUTES.items():
        if incoming_path.startswith(route_prefix):
            service_url = backend + incoming_path
            break
    
    if not service_url:
        return jsonify({"error": "No backend service found"}), 404
    
    # Forward request
    try:
        upstream = requests.request(
            method=request.method,
            url=service_url,
            headers=dict(request.headers),
            params=dict(request.args),
            json=request.get_json(silent=True),
            timeout=1
        )

        response = make_response(upstream.content, upstream.status_code)
        for key, value in upstream.headers.items():
            response.headers[key] = value

        return response, 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Service unreachable", "details": str(e)}), 502


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
