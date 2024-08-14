"""
Module to handle connection with MySQL
"""

import mysql.connector

# Global variable to hold MySQL connection object
__cnx = None


def get_sql_connection():
    """
    Establish and return a MySQL connection.
    Output: a MySQL connection object
    """
    global __cnx

    if __cnx is None:
        __cnx = mysql.connector.connect(
            user="root", password="", host="127.0.0.1", database="gs"
        )

    return __cnx
