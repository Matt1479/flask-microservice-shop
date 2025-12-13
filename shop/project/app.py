import os
import utils
from flask import Flask, jsonify, request
from typing import Any


app = Flask(__name__)
port = int(os.environ.get("PORT", 5002))

PRODUCTS: list[dict[str, Any]] = utils.init_products()


@app.route("/api/shop")
def shop():
    return jsonify({"message": "Hello, this is Shop Service"}), 200


@app.route("/api/shop/products", methods=["GET"])
def get_products():
    return jsonify({"data": PRODUCTS}), 200 if PRODUCTS else 204


@app.route("/api/shop/products/<id>", methods=["GET"])
def get_product(id: int):
    if not utils.validate_int(id):
        return jsonify({"error": "id must be an integer"}), 400
    id = int(id)

    for product in PRODUCTS:
        if product.get("id") == id:
            return jsonify({"data": product}), 200
    return jsonify({"error": f"Product of id {id} is not found."}), 404


@app.route("/api/shop/products/add", methods=["POST"])
@utils.user_id_admin_role_required
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

    if not utils.validate_float(data["price"]):
        return jsonify({"error": "Price must be a real number"}), 400
    
    if not utils.validate_int(data["stock"]):
        return jsonify({"error": "Stock must be an integer"}), 400
    
    data["id"] = max([product["id"] for product in PRODUCTS]) + 1 if PRODUCTS else 1
    PRODUCTS.append(data)
    return jsonify({"message": "Product added successfully"}), 200


@app.route("/api/shop/products/delete/<id>", methods=["DELETE"])
@utils.user_id_admin_role_required
def delete_product(id: int):
    if not utils.validate_int(id):
        return jsonify({"error": "id must be an integer"}), 400
    id = int(id)

    for product in PRODUCTS:
        if product.get("id") == id:
            PRODUCTS.remove(product)
            return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"error": f"Product of id {id} is not found."}), 404


@app.route("/api/shop/products/update", methods=["PUT"])
@utils.user_id_admin_role_required
def update_product():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    if not utils.validate_int(data["id"]):
        return jsonify({"error": "id must be an integer"}), 400

    for product in PRODUCTS:
        if product["id"] == data["id"]:
            product.update(data)
            return jsonify({"message": "Product updated successfully"}), 200
    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
