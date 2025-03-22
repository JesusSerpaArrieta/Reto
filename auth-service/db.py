import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        user="root",
        password="",
        host="127.0.0.1",
        database="mydb"
    )
