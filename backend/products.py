"""
Products DAO (Data Access Object)
"""

import mysql.connector

cnx = mysql.connector.connect(user="root", password="", host="127.0.0.1", database="gs")

cursor = cnx.cursor()
query: str = "SELECT * FROM gs.products"
cursor.execute(query)

for (product_id, name, uom_id, price_per_unit) in cursor:
    print(product_id, name, uom_id, price_per_unit)

cnx.close()
