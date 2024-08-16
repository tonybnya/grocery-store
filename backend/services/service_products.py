"""
Products DAO (Data Access Object)
"""

from typing import Dict, List, Optional, Tuple, Union

from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor import MySQLCursor


def get_all_products(
    cnx: MySQLConnection,
) -> Optional[List[Dict[str, Union[int, str, float]]]]:
    """
    Fetch all the products from the MySQL database.

    Input:  cnx (MySQLConnection)     | a MySQL connection object
    Output: a list of dictionaries of products or None
    """
    # Define a string as a query to fetch all the products from the database
    # and join with each product with its corresponding Unit of Measure (uom)
    query: str = (
        "SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name FROM products INNER JOIN uom ON products.uom_id=uom.uom_id"
    )

    try:
        # Define an instance of the MySQL cursor
        cursor: MySQLCursor = cnx.cursor()

        # Execute the defined query
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
    except Error as e:
        print(f"Error fetching products: {e}")
        return None


def get_single_product(
    cnx: MySQLConnection, product_id: int
) -> Optional[Dict[str, Union[int, str, float]]]:
    """
    Retrieves a single product from the database by its ID.

    Input:  cnx (MySQLConnection)   | a MySQL connection object
    Input:  product_id (int)        | the ID of the product to update
    Output: a dictionary containing the product details if found or None
    """
    # Define the query string to retrieve the product needed
    query: str = "SELECT * FROM products WHERE products.product_id = %s"

    try:
        # Define an instance of the MySQL cursor
        cursor: MySQLCursor = cnx.cursor(dictionary=True)

        # Execute the defined query
        cursor.execute(query, (product_id,))

        # Fetch the selected product
        product: Dict[str, Union[int, str, float]] = cursor.fetchone()

        return product
    except Error as e:
        print(f"Error fetching product: {e}")
        return None


def insert_new_product(
    cnx: MySQLConnection, product: Dict[str, Union[int, str, float]]
) -> Optional[int]:
    """
    Insert a new product into the database.

    Input:  cnx (MySQLConnection)   | a MySQL connection object
    Input:  product (dict)          | a dictionary representing the product to insert
    Output: the number of records into the table or None
    """
    # Define an instance of the MySQL cursor
    cursor: MySQLCursor = cnx.cursor()

    # Define a string representing a query
    # to insert a new product into the database
    query: str = (
        "INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)"
    )

    # Use the product dictionary provided to build
    # a tuple containing data to record/insert into the database
    data: Tuple[Union[int, str, float]] = (
        product["name"],
        product["uom_id"],
        product["price_per_unit"],
    )

    # Execute the query with the corresponding data
    cursor.execute(query, data)
    cnx.commit()

    return cursor.lastrowid


def update_product(
    cnx: MySQLConnection,
    product_id: int,
    updated_data: Dict[str, Union[int, str, float]],
) -> int:
    """
    Update an existing product in the database.

    Input:  cnx (MySQLConnection)   | a MySQL connection object
    Input:  product_id (int)        | the ID of the product to update
    Input:  updated_data (dict)     | a dictionary representing the updated product data
    Output: the number of records affected
    """
    # Define an instance of the MySQL cursor
    cursor: MySQLCursor = cnx.cursor()

    # Construct the SQL query for updating the product
    query: str = (
        "UPDATE products SET name = %s, uom_id = %s, price_per_unit = %s WHERE product_id = %s"
    )

    data: Tuple[Union[int, str, float]] = (
        updated_data["name"],
        updated_data["uom_id"],
        updated_data["price_per_unit"],
        product_id,
    )

    # Execute the query with the corresponding data
    cursor.execute(query, data)
    cnx.commit()

    return cursor.rowcount


def delete_product(cnx: MySQLConnection, product_id: int) -> int:
    """
    Delete a product from the database.

    Input:  cnx (MySQLConnection)   | a MySQL connection object
    Input:  product_id (int)        | the ID of the product to delete
    Output: the number of records affected
    """
    # Define an instance of the MySQL cursor
    cursor: MySQLCursor = cnx.cursor()

    # Construct the SQL query for deleting the product
    query: str = "DELETE FROM products WHERE product_id = %s"

    # Execute the query with the corresponding product_id
    cursor.execute(query, (product_id,))
    cnx.commit()

    return cursor.rowcount
