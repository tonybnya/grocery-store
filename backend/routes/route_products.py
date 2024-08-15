"""
Product routes for the Grocery Management System API.
"""

from typing import Dict, List, Union

from flask import Blueprint, jsonify
from flask.blueprints import BlueprintSetupState
from mysql.connector import MySQLConnection
from services import service_products

# Create a blueprint for product-related routes
products_blueprint = Blueprint("products", __name__)

# Assuming `cnx` is passed when the blueprint is registered
cnx: MySQLConnection


@products_blueprint.record
def record_params(setup_state: BlueprintSetupState):
    """
    A callback function that runs when the blueprint is registered.

    This function retrieves the MySQL connection object from the Flask
    app's configuration and assigns it to the global variable `cnx`
    within the blueprint. This ensures that the connection object is
    available to all routes within this blueprint.

    Args:
        setup_state (BlueprintSetupState): The setup state object
        provided by Flask, which includes the app context and configuration
        information when the blueprint is being registered.
    """
    global cnx
    cnx = setup_state.app.config["cnx"]


@products_blueprint.route("/products", methods=["GET"])
def get_products():
    """
    GET /products
    READ/GET all the products from the API.
    """
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
