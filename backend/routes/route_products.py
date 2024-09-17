"""
Product routes/endpoints for the Grocery Management System API.
"""

from typing import Dict, List, Literal, Optional, Tuple, Union

from flask import Blueprint, Response, current_app, jsonify, make_response, request
from mysql.connector import MySQLConnection
from services import service_products

# Create a Blueprint for all the products
all_products_bp: Blueprint = Blueprint("all_products_bp", __name__)

# Create a Blueprint for a single product
single_product_bp: Blueprint = Blueprint("single_product_bp", __name__)

# Create a Blueprint for a product insertion
insert_product_bp: Blueprint = Blueprint("insert_product_bp", __name__)

# Create a Blueprint for a product update
update_product_bp: Blueprint = Blueprint("update_product_bp", __name__)

# Create a Blueprint for a product deletion
delete_product_bp: Blueprint = Blueprint("delete_product_bp", __name__)


@all_products_bp.route("/products", methods=["GET"])
def get_all_products() -> Union[Response, Tuple[Response, Literal[404]]]:
    """
    GET /products
    READ all the products from the API.

    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Get the list of all the products from the database
    products: Optional[List[Dict[str, Union[int, str, float]]]] = (
        service_products.get_all_products(cnx)
    )

    # Declare a variable to hold the Flask response object
    response: Union[Response, Tuple[Response, Literal[404]]]

    if products:
        # Create a Flask response object
        response = make_response(jsonify(products), 200)
    else:
        # Create a response with a 404 error if the products are not found
        response = make_response(jsonify({"error": "Products not found"}), 404)

    # The `Access-Control-Allow-Origin header` is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    # `*` means that all the origins can access the endpoint.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@single_product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_single_product(
    product_id: int,
) -> Union[Response, Tuple[Response, Literal[404]]]:
    """
    GET /products/{product_id}
    READ a single product by its ID

    Input: product_id (int) | the ID of the product to fetch
    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Fetch the product details from the database
    product: Optional[Dict[str, Union[int, str, float]]] = (
        service_products.get_single_product(cnx, product_id)
    )

    # Declare a variable to hold the Flask response object
    response: Union[Response, Tuple[Response, Literal[404]]]

    if product:
        # Create a Flask response object
        response = make_response(jsonify(product), 200)
    else:
        # Create a response with a 404 error if the product is not found
        response = make_response(jsonify({"error": "Product not found"}), 404)

    # The `Access-Control-Allow-Origin` header is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    # `*` means that all the origins can access the endpoint.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@insert_product_bp.route("/products", methods=["POST"])
def insert_product() -> Union[Response, Tuple[Response, Literal[400]]]:
    """
    POST /products
    CREATE a new product

    Input: the request body, a JSON object representing the product to insert
    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Parse the JSON data from the request body
    product_data: Dict[str, Union[int, str, float]] = request.get_json()

    # Declare a variable to hold the Flask response object
    response: Union[Response, Tuple[Response, Literal[400]]]

    # Validate the incoming data from the request body
    required_fields: List[str] = ["name", "uom_id", "price_per_unit"]
    for field in required_fields:
        if field not in product_data:
            return make_response(
                jsonify({"error": f"Missing required field: {field}"}), 400
            )
    if product_id := service_products.insert_new_product(cnx, product_data):
        # Create a success response with the newly created product ID
        response = make_response(
            jsonify({"message": "Product created", "product_id": product_id}), 201
        )
    else:
        # Create a response with a 400 error if the insertion failed
        response = make_response(jsonify({"error": "Failed to insert product"}), 400)

    # The `Access-Control-Allow-Origin` header is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    # `*` means that all the origins can access the endpoint.
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
    updated_product: Dict[str, Union[int, str, float]] = request.get_json()

    # Declare a variable to hold the Flask response object
    response: Union[Response, Tuple[Response, Literal[400]]]

    # Validate the incoming data from the request body
    required_fields: List[str] = ["name", "uom_id", "price_per_unit"]
    for field in required_fields:
        if field not in updated_product:
            return make_response(
                jsonify({"error": f"Missing required field: {field}"}), 400
            )
    # Validate the incoming data from the request body
    # required_fields: List[str] = ["name", "uom_id", "price_per_unit"]
    # for field in required_fields:
    #     if field not in updated_data:
    #         response = make_response(
    #             jsonify({"error": f"Missing required field: {field}"}), 400
    #         )
    #         return response

    # Update the product in the database
    rows_affected: int = service_products.update_product(
        cnx, product_id, updated_product
    )

    if rows_affected > 0:
        # Create a success response with the number of rows affected
        response = jsonify(
            {"message": "Product updated successfully", "product": updated_product}
        )
    else:
        return make_response(
            jsonify({"error": "Failed to update product or product not found"}),
            400,
        )
    # The `Access-Control-Allow-Origin` header is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    # `*` means that all the origins can access the endpoint.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@delete_product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> Union[Response, Tuple[Response, Literal[404]]]:
    """
    DELETE /products/{product_id}
    DELETE a product by its ID

    Input: product_id (int) | the ID of the product to delete
    Output: a Flask Response object
            including HTTP status code, JSON data, and CORS headers
    """
    # Get the database connection from the app config
    cnx: MySQLConnection = current_app.config["cnx"]

    # Delete the product from the database
    rows_affected: int = service_products.delete_product(cnx, product_id)

    if rows_affected > 0:
        # Create a success response indicating the product was deleted
        response = make_response(jsonify({"message": "Product deleted successfully"}))
    else:
        # Create a response with a 404 error if the product was not found
        response = make_response(jsonify({"error": "Product not found"}), 404)

    # The `Access-Control-Allow-Origin` header is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    # `*` means that all the origins can access the endpoint.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response
