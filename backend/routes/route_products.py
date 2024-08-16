"""
Product routes for the Grocery Management System API.
"""

from typing import Dict, List, Literal, Optional, Tuple, Union

from flask import Blueprint, Response, current_app, jsonify
from mysql.connector import MySQLConnection
from services import service_products

# Create a Blueprint for all the products
all_products_bp = Blueprint("all_products_bp", __name__)

# Create a Blueprint for a single product
single_product_bp: Blueprint = Blueprint("single_product_bp", __name__)


@all_products_bp.route("/products", methods=["GET"])
def get_all_products() -> Response:
    """
    GET /products
    READ/GET all the products from the API.

    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Get the list of all the products from the database
    products: Optional[List[Dict[str, Union[int, str, float]]]] = (
        service_products.get_all_products(cnx)
    )

    if products:
        # Formatting the list of products into JSON
        response: Response = jsonify(products)
    else:
        # Return a 404 error if the product is not found
        response = jsonify({"error": "Product not found"}), 404

    # The `Access-Control-Allow-Origin header` is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@single_product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_single_product(
    product_id: int,
) -> Union[Response, Tuple[Response, Literal[404]]]:
    """
    GET /products/{product_id}
    READ/GET a single product by its ID

    Input: product_id (int) | the ID of the product to fetch
    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Fetch the product details from the database
    product = service_products.get_single_product(cnx, product_id)

    if product:
        # Formatting the product details into JSON
        response: Response = jsonify(product)
    else:
        # Return a 404 error if the product is not found
        response = jsonify({"error": "Product not found"}), 404

    # The `Access-Control-Allow-Origin` header is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response
