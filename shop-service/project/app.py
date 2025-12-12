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
            "id": product.get("id"),
            "title": product.get("title"),
            "description": product.get("description"),
            "category": product.get("category"),
            "price": product.get("price"),
            "stock": product.get("stock"),
            "images": product.get("images"),
            "thumbnail": product.get("thumbnail"),
        })
    return products


PRODUCTS: list[dict[str, Any]] = init_products()


@app.route("/api/shop")
def shop():
    return jsonify({"message": "Hello, this is Shop Service"}), 200


@app.route("/api/shop/products", methods=["GET"])
def get_products():
    return jsonify({"data": PRODUCTS}), 200 if PRODUCTS else 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
