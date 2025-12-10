from flask import render_template

from app.products import bp


@bp.route("/")
def list_products():
    """
    Simple products list that demonstrates work of products blueprint.
    """
    products = [
        {"id": 1, "name": "Flask Course", "price": 0, "in_stock": True},
        {"id": 2, "name": "Python Book", "price": 500, "in_stock": True},
        {"id": 3, "name": "Java Backend Workshop", "price": 1000, "in_stock": False},
    ]
    return render_template("products/list.html", products=products)
