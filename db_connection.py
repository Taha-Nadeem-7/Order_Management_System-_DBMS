

# db_connection.py
import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="",      # or your MySQL user
        password="",      # or your MySQL password
        database="restaurant_db"
    )
