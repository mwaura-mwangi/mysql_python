import os
from pathlib import Path
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

#load database credentioals from .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def main():
    # load csv files into DataFrames
    print("Loading CSV files..,")
    df1 = pd.read_csv("coffee_sales_1.csv")
    df2 = pd.read_csv("coffee_sales_2.csv")

    # Ensure coffee_sales_2 has a card column with None?NaN values for consistency.
    if 'card' not in df2.columns:
        df2['card'] = None

    # Align column order and combine Dataframes
    columns = ['date', 'datetime', 'cash_type', 'card', 'money', 'coffee_name']
    df_combined = pd.concat([df1[columns]], ignore_index=True)

    #convert NaNs to None for MySQL NULL handling
    df_combined = df_combined.where(pd.notnull(df_combined), None)

    print(f"Total records to insert: {len(df_combined)}")

    # initialize connection objects for clean exception handling
    connection = None
    cursor = None

    # connect to mysql
    try:
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST", "localhost"),
            user = os.getenv("DB_USER", "root"),
            password = os.getenv("DB_PASSWORD")
        )
        cursor = connection.cursor()

        # create database and table if they dont exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS coffee_shop;")
        cursor.execute("USE coffee_shop;")


        create_table_query = """
        CREATE TABLE IF NOT EXISTS coffee_sales(
            id INT AUTO_INCREMENT PRIMARY KEY,
            sale_date DATE NOT NULL,
            sale_datetime DATETIME NOT NULL,
            cash_type VARCHAR(20) NOT NULL,
            card_number VARCHAR(50) DEFAULT NULL,
            money DECIMAL (10, 2) NOT NULL,
            coffee_name VARCHAR(100) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        print("Database and table ready.")

        # Batch insert records
        insert_query = """
        INSERT INTO coffee_sales (sale_date, sale_datetime, cash_type, card_number, money, coffee_name)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        #convert DataFrame rows into a list of tuples
        data_to_insert = [tuple(row) for row in df_combined.to_numpy()]

        cursor.executemany(insert_query, data_to_insert)
        connection.commit()

        print(f"Successfully inserted {cursor.rowcount} rows into 'coffee_sales' table. ")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()


