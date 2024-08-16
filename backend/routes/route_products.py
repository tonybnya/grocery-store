"""
Product routes for the Grocery Management System API.
"""

from typing import Dict, List, Union

from flask import Blueprint, current_app, jsonify
from services import service_products

# Create a Blueprint for products
products_bp = Blueprint("products_bp", __name__)


@products_bp.route("/products", methods=["GET"])
def get_products():
    """
    GET /products
    READ/GET all the products from the API.
    """
    # Get the database connection from the app config
    cnx = current_app.config["cnx"]

    # Get the list of all the products from the database
    products: List[Dict[str, Union[int, str, float]]] = (
        service_products.get_all_products(cnx)
    )

    # Formatting the list of products into JSON
    response = jsonify(products)

    # The `Access-Control-Allow-Origin header` is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response
