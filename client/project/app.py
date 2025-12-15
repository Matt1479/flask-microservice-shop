import os
from flask import Flask, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))


@app.route("/")
def index():
    return jsonify({"message": "Hello, this is client"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
