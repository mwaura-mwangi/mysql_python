import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv


# load .env file from the current directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# retrieve variables
db_host = os.getenv("DB_HOST", "localhost")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD")

# debug out put to verify what is actually loaded
print(f"Connecting as user: {db_user}")
print(f"Password detected: {'YES' if db_password else 'NO'}")

# initializa connection
connection = None

try:
    connection = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password
    )

    if connection.is_connected():
        print("Connected to MYSQL version:", connection.get_server_info())

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")

