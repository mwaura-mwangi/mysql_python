import os
import mysql.connector
from dotenv import load_dotenv


try:
    connection = mysql.connector.connect(
        host = os.getenv("DB_HOST", "localhost"),
        user = os.getenv("DB_USER", "root"),
        password = os.getenv("DB_PASSWORD")
    )

    if connection.is_connected():
        print("Connected to MYSQL version:", connection.get_server_info())

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()