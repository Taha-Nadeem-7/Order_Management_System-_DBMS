

# db_connection.py
import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="taha",      # or your MySQL user
        password="taha2005",      # or your MySQL password
        database="restaurant_db"
    )
