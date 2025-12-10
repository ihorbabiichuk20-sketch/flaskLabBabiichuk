from flask import render_template
from . import products_bp

# Проста заглушка списку продуктів для демонстрації блюпринта (ЛР3).

PRODUCTS = [
    {"id": 1, "name": "Ноутбук Lenovo", "price": 25000},
    {"id": 2, "name": "Ноутбук Dell", "price": 32000},
    {"id": 3, "name": "Ноутбук HP", "price": 28000},
]


@products_bp.route("/")
def list_products():
    return render_template("products/list.html", products=PRODUCTS)
