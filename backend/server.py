"""
Main application performing the Flask Server.
Definition of all the endpoints of the API.
"""

from database.sql_connection import get_sql_connection
from flask import Flask
from mysql.connector import MySQLConnection
from routes import route_products

app = Flask(__name__)

# Define a MySQL connection object as a global variable
# to hold the connection with the MySQL database
cnx: MySQLConnection = get_sql_connection()

# Store the MySQL connection object in the app's config
app.config["cnx"] = cnx


@app.route("/")
def root():
    """
    Root endpoint for the Grocery Management System API.

    This endpoint returns a simple JSON message indicating that the
    Grocery Management System API is running. It serves as a basic
    health check or welcome message.

    Output: a JSON object with a welcome message.
    """
    return {"message": "Welcome to the Grocery Store Management System API!"}


# Register the product routes
app.register_blueprint(route_products.all_products_bp)
app.register_blueprint(route_products.single_product_bp)


if __name__ == "__main__":
    print("Starting Flask Server for Grocery Management System...")
    app.run(debug=True)
