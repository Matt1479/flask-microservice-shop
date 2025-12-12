import requests
import os
from flask import Flask, jsonify
from typing import Any


app = Flask(__name__)
port = int(os.environ.get("PORT", 5002))


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


@app.route("/api/shop/product/<id>", methods=["GET"])
def get_product(id: int):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": f"id must be an integer."}), 400

    for product in PRODUCTS:
        if product.get("id") == id:
            return jsonify({"data": product}), 200
    return jsonify({"error": f"Product of id {id} is not found."}), 404


@app.route("/api/shop/products", methods=["GET"])
def get_products():
    return jsonify({"data": PRODUCTS}), 200 if PRODUCTS else 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
