"""
Products DAO (Data Access Object)
"""

from typing import Dict, List, Tuple, Union

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

    return products


def insert_new_product(
    cnx: MySQLConnection, product: Dict[str, Union[int, str, float]]
):
    """
    Insert a new product into the database.
    Input:  cnx     | a MySQL connection object
    Input:  product | a dictionary representing the product to insert
    Output: the last record of the products table
    """
    # Define an instance of the MySQL cursor
    cursor: MySQLCursor = cnx.cursor()

    # Define a string representing a query
    # to insert a new product into the database
    query: str = (
        "INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)"
    )

    data: Tuple[Union[int, str, float]] = (
        product["name"],
        product["uom_id"],
        product["price_per_unit"],
    )

    # Execute the query with the corresponding data
    cursor.execute(query, data)
    cnx.commit()

    return cursor.lastrowid


if __name__ == "__main__":
    cnx = get_sql_connection()

    products: List[Dict[str, Union[str, float]]] = get_all_products(cnx)
    print(products[-1])

    new_product: Dict[str, Union[str, float]] = {
        "name": "milk (bottle)",
        "uom_id": 2,
        "price_per_unit": 3200,
    }

    insert_new_product(cnx, new_product)

    products: List[Dict[str, Union[str, float]]] = get_all_products(cnx)
    print(products[-1])
