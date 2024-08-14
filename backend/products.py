"""
Products DAO (Data Access Object)
"""

import pprint
from typing import Dict, List, Union

from sql_connection import get_sql_connection


def get_all_products(cnx):
    cursor = cnx.cursor()
    # query: str = "SELECT * FROM gs.products"
    query: str = (
        "SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name FROM products INNER JOIN uom ON products.uom_id=uom.uom_id"
    )
    cursor.execute(query)

    response: List[Dict[str, Union[str, float]]] = []

    for product_id, name, uom_id, price_per_unit, uom_name in cursor:
        response.append(
            {
                "Product ID": product_id,
                "Product Name": name,
                "UOM ID": uom_id,
                "Price per Unit": price_per_unit,
                "Unit of Measure": uom_name,
            }
        )
        print(product_id, name, uom_id, price_per_unit, uom_name)

    cnx.close()

    return response


if __name__ == "__main__":
    cnx = get_sql_connection()
    products: List[Dict[str, Union[str, float]]] = get_all_products(cnx)

    for product in products:
        print(product)
        print()
