import jwt
import os
import requests
from flask import Flask, g, jsonify, make_response, request


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
port = int(os.environ.get("PORT", 5000))

SERVICE_ROUTES = {
    "/api/auth": "http://localhost:5001",
    "/api/shop": "http://localhost:5002",
    "/api/logs": "http://localhost:5003"
}
PUBLIC_ROUTES = [
    "/api/auth"
]


@app.before_request
def check_auth():
    # Skip token check for public routes
    if any(request.path.startswith(p) for p in PUBLIC_ROUTES):
        return

    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Authorization token is missing"}), 401
    
    try:
        data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        return jsonify({"error": "Authorization token is invalid"}), 401
    
    g.user_id = str(data.get("user_id"))
    g.user_role = data.get("user_role")


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
        forward_headers = dict(request.headers)

        # Strip spoofable headers
        for h in ["x_user_id", "x_user_role"]:
            forward_headers.pop(h, None)
        
        # Inject trusted identity headers
        if hasattr(g, "user_id"):
            forward_headers["x_user_id"] = g.user_id
        if hasattr(g, "user_role"):
            forward_headers["x_user_role"] = g.user_role

        upstream = requests.request(
            method=request.method,
            url=service_url,
            headers=forward_headers,
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
