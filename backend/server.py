"""
Main application performing the Flask Server.
Definition of all the endpoints of the API.
"""

from typing import Dict, List, Union

import dao_products
from flask import Flask, jsonify
from mysql.connector import MySQLConnection
from sql_connection import get_sql_connection

app = Flask(__name__)

# Define a MySQL connection object as global variable
# to hold the connection with the MySQL database
cnx: MySQLConnection = get_sql_connection()


@app.route("/")
def root():
    return {"message": "Grocery Management System"}


@app.route("/products", methods=["GET"])
def get_products():
    """
    GET /products
    READ/GET all the products from the API.
    """
    # Get the list of all the products from the database
    products: List[Dict[str, Union[int, str, float]]] = dao_products.get_all_products(
        cnx
    )

    # Formatting the list of products into JSON
    response = jsonify(products)

    # The `Access-Control-Allow-Origin header` is part of the CORS mechanism.
    # It tells the browser which origins are allowed to access
    # the resources on the server.
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


if __name__ == "__main__":
    print("Starting Flask Server for Grocery Management System...")
    app.run(debug=True)
