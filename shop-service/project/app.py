import requests
import os
from flask import Flask, jsonify, request
from typing import Any


app = Flask(__name__)
port = int(os.environ.get("PORT", 5002))


def validate_int(value):
    try:
        return int(value)
    except ValueError:
        return False


def validate_float(value):
    try:
        return float(value)
    except ValueError:
        return False


def init_products() -> list[dict[str, Any]]:
    data = requests.get("https://dummyjson.com/products").json()
    
    products = []
    for product in data["products"]:
        products.append({
            "id": int(product.get("id")),
            "title": product.get("title"),
            "description": product.get("description"),
            "category": product.get("category"),
            "price": float(product.get("price")),
            "stock": int(product.get("stock"))
        })
    return products


PRODUCTS: list[dict[str, Any]] = init_products()


@app.route("/api/shop")
def shop():
    return jsonify({"message": "Hello, this is Shop Service"}), 200


@app.route("/api/shop/products/<id>", methods=["GET"])
def get_product(id: int):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": "id must be an integer."}), 400

    for product in PRODUCTS:
        if product.get("id") == id:
            return jsonify({"data": product}), 200
    return jsonify({"error": f"Product of id {id} is not found."}), 404


@app.route("/api/shop/products", methods=["GET"])
def get_products():
    return jsonify({"data": PRODUCTS}), 200 if PRODUCTS else 204


@app.route("/api/shop/products/add", methods=["POST"])
def add_product():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    if (
        not data.get("title")
        or not data.get("description")
        or not data.get("category")
        or not data.get("price")
        or not data.get("stock")
    ):
        return jsonify({"error": "Missing required field(s)"}), 400

    if not validate_float(data["price"]):
        return jsonify({"error": "Price must be a real number"}), 400
    
    if not validate_int(data["stock"]):
        jsonify({"error": "Stock must be an integer"}), 400
    
    data["id"] = max([product["id"] for product in PRODUCTS]) + 1
    PRODUCTS.append(data)
    return jsonify({"message": "Product added successfully"}), 200


@app.route("/api/shop/products/update", methods=["PUT"])
def update_product():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    if not validate_int(data["id"]):
        return jsonify({"error": "id must be a real number"}), 400

    for product in PRODUCTS:
        if product["id"] == data["id"]:
            product.update(data)
    return jsonify({"message": "Product updated successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
