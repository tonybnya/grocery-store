"""
Module to handle connection with the MySQL database
"""

from mysql.connector import MySQLConnection, connect

# Global variable to hold a MySQL connection object
__cnx: MySQLConnection = None


def get_sql_connection() -> MySQLConnection:
    """
    Establish and return a MySQL connection.
    Output: a MySQL connection object
    """
    global __cnx

    if __cnx is None:
        __cnx = connect(user="root", password="", host="127.0.0.1", database="gs")

    return __cnx
