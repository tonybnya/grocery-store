"""
Products DAO (Data Access Object)
"""

from typing import Dict, List, Union

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from sql_connection import get_sql_connection


def get_all_products(cnx: MySQLConnection) -> List[Dict[str, Union[int, str, float]]]:
    """
    Fetch all the products from the MySQL database.
    Input:  cnx     | a MySQL connection object
    Output: a list of dictionaries
    """
    # Define an instance of the MySQL cursor
    cursor: MySQLCursor = cnx.cursor()

    # Define a string as a query to fetch all the products from the database
    # and join with each product with its corresponding Unit of Measure (uom)
    query: str = (
        "SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name FROM products INNER JOIN uom ON products.uom_id=uom.uom_id"
    )
    cursor.execute(query)

    # Define a list of dictionaries to hold all the products
    # Dictonary keys should be strings
    # Dictonary values could be either integers, strings or floats
    products: List[Dict[str, Union[int, str, float]]] = []

    # Traverse records (tuples) and append elements as dictionaries
    # into the predefined products list
    for product_id, name, uom_id, price_per_unit, uom_name in cursor:
        products.append(
            {
                "product_id": product_id,
                "name": name,
                "uom_id": uom_id,
                "price_per_unit": price_per_unit,
                "uom_name": uom_name,
            }
        )

    # Close the cursor & the connection to the database
    cursor.close()
    cnx.close()

    return products


def insert_new_product(cnx, product):
    pass


if __name__ == "__main__":
    cnx = get_sql_connection()
    products: List[Dict[str, Union[str, float]]] = get_all_products(cnx)
    print(products)
