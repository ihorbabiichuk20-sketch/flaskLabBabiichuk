from flask import Blueprint, render_template

products_bp = Blueprint("products", __name__)

# Демонстраційний список ноутбуків
NOTEBOOKS = [
    {"id": 1, "brand": "Dell", "model": "XPS 13", "price": 1200},
    {"id": 2, "brand": "Apple", "model": "MacBook Air", "price": 1400},
    {"id": 3, "brand": "Lenovo", "model": "ThinkPad X1 Carbon", "price": 1300},
]

@products_bp.route("/")
def list_products():
    return render_template("products/list.html", notebooks=NOTEBOOKS)