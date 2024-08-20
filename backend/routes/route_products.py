"""
Product routes for the Grocery Management System API.
"""

from typing import Dict, List, Literal, Optional, Tuple, Union

from flask import (Blueprint, Response, current_app, jsonify, make_response,
                   request)
from mysql.connector import MySQLConnection
from services import service_products

# Create a Blueprint for all the products
all_products_bp = Blueprint("all_products_bp", __name__)

# Create a Blueprint for a single product
single_product_bp: Blueprint = Blueprint("single_product_bp", __name__)

# Create a Blueprint for product insertion
insert_product_bp: Blueprint = Blueprint("insert_product_bp", __name__)

# Create a Blueprint for product update
update_product_bp: Blueprint = Blueprint("update_product_bp", __name__)

# Create a Blueprint for product deletion
delete_product_bp: Blueprint = Blueprint("delete_product_bp", __name__)


@all_products_bp.route("/products", methods=["GET"])
def get_all_products() -> Union[Response, Tuple[Response, Literal[404]]]:
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

    response: Union[Response, Tuple[Response, Literal[404]]]

    if products:
        # Formatting the list of products into JSON
        response = make_response(jsonify(products), 200)
    else:
        # Return a 404 error if the product is not found
        response = make_response(jsonify({"error": "Product not found"}), 404)

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

    response: Union[Response, Tuple[Response, Literal[404]]]

    if product:
        # Formatting the product details into JSON
        response = make_response(jsonify(product), 200)
    else:
        # Return a 404 error if the product is not found
        response = make_response(jsonify({"error": "Product not found"}), 404)

    # The `Access-Control-Allow-Origin` header is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@insert_product_bp.route("/products", methods=["POST"])
def insert_product() -> Union[Response, Tuple[Response, Literal[400]]]:
    """
    POST /products
    CREATE/POST a new product

    Input: a JSON object representing the product to insert
    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Parse the JSON data from the request body
    product_data: Dict[str, Union[int, str, float]] = request.get_json()

    response: Union[Response, Tuple[Response, Literal[400]]]

    # Validate the incoming data from the request body
    required_fields: List[str] = ["name", "uom_id", "price_per_unit"]
    for field in required_fields:
        if field not in product_data:
            response = jsonify({"error": f"Missing required field: {field}"})
            return response, 400

    # Insert the product into the database
    product_id: Optional[int] = service_products.insert_new_product(cnx, product_data)

    if product_id:
        # Return a success response with the newly created product ID
        response = make_response(
            jsonify({"message": "Product created", "product_id": product_id}), 201
        )
        # response.status_code = 201
    else:
        # Return an error response if the insertion failed
        response = make_response(jsonify({"error": "Failed to insert product"}), 400)
        # return response, 400

    # Add CORS headers
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@update_product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> Union[Response, Tuple[Response, Literal[400]]]:
    """
    PUT /products/{product_id}
    UPDATE a single product by its ID

    Input: product_id (int) | the ID of the product to update
    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Parse the JSON data from the request body
    updated_data: Dict[str, Union[int, str, float]] = request.get_json()

    response: Union[Response, Tuple[Response, Literal[400]]]

    # Validate the incoming data from the request body
    required_fields: List[str] = ["name", "uom_id", "price_per_unit"]
    for field in required_fields:
        if field not in updated_data:
            response = jsonify({"error": f"Missing required field: {field}"})
            return response, 400

    # Update the product in the database
    rows_affected: int = service_products.update_product(cnx, product_id, updated_data)

    if rows_affected > 0:
        # Return a success response with the number of rows affected
        response = jsonify({"message": "Product updated successfully"})
    else:
        # Return an error response if the update failed
        response = jsonify({"error": "Failed to update product or product not found"})
        return response, 400

    # Add CORS headers
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@delete_product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product():
    pass
