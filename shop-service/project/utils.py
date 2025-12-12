import requests
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
