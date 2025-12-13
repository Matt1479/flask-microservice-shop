import requests
from flask import jsonify, request
from functools import wraps
from typing import Any


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


def user_id_admin_role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.headers.get("X-User-Id"):
            return jsonify({"error": "user id is required"}), 401

        user_role = request.headers.get("X-User-Role")

        if not user_role:
            return jsonify({"error": "user role is required"}), 401
        
        if user_role != "admin":
            return jsonify({"error": "You have insufficient rights to access this resource"}), 403
        
        return f(*args, **kwargs)
    
    return decorated
