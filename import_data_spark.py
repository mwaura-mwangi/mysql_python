import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "coffee_shop_parkroad"


def prepare_mysql_database():
     """Ensure target database and table exist before spark JDBC """
     print(f"Ensuring database {DB_NAME} exists in mysql")
     conn = mysql.connector.connect(
          host=DB_HOST,
          user=DB_USER,
          password=DB_PASSWORD
     )
     cursor = conn.cursor()


     #create the new database if it doesnt exist
     cursor.execute(f"CREATE DATABASE IF NOT EXIST {DB_NAME}:")
     cursor.execute(f"USE {DB_NAME}:")

     # Create table target schema
     create_table_query = """
    CREATE TABLE IF NOT EXISTS coffee_sales_parkroad(
        id INT AUTO_INCREMENT PRIMARY KEY,
        sale_date DATE NOT NULL,
        sale_datetime DATETIME NOT NULL,
        cash_type VARCHAR(20) NOT NULL,
        card_number VARCHAR(50) DEFAULT NULL,
        money DECIMAL(10, 2) NOT NULL,
        coffee_name VARCHAR(100) NOT NULL
        );
        """

     cursor.execute(create_table_query)
     conn.commit()
     cursor.close()
     conn.close()
     print(f"Database '{DB_NAME}' and table 'coffee_sales_parkroad' are ready.")


def main():
    print("Initializing spark session...")
    # Initialize spark with the maven package for mysql jdbc
    builder = SparkSession.builder
    spark = (
         builder
        .appName("CoffeeSalesETL_PySpark_Parkroad")
        .config("spark.jars.packages", "com.mysql:mysql-connector-j:9.1.0")
        .getOrCreate()
    )

    # Mute verbose spark logs
    spark.sparkContext.setLogLevel("ERROR")

    print("Loading CSV datasets with PySpark...")
    # Read CSVs (PySpark handles wildcard path ingestion automatically)
    df1 = spark.read.option("header", "true").csv("coffee_sales_1.csv")
    df2 = spark.read.option("header", "true").csv("coffee_sales_2.csv")

    # Add missing 'card' column to df2 as NULL if it doesnt exist
    if "card" not in df2.columns:
        df2 = df2.withColumn("card", F.lit(None))

    # Align columns and unify DataFrames
    columns = ["date", "datetime", "cash_type", "card", "money", "coffee_name"]
    df_combined = df1.select(*columns).union(df2.select(*columns))

    # Rename columns to match target MySQL table schema & cast data types
    df_transformed = df_combined \
        .withColumnRenamed("date", "sale_date")\
        .withColumnRenamed("datetime", "sale_datetime")\
        .withColumnRenamed("card", "card_number") \
        .withColumn("sale_date", F.to_date(F.col("sale_date")))\
        .withColumn("sale_datetime", F.to_timestamp(F.col("sale_datetime")))\
        .withColumn("money", F.col("money").cast("decimal(10,2)"))

    print(f"Total PySpark records to load: {df_transformed.count()}")

    # MySql JDBC Configuration
    jdbc_url = f"jdbc:mysql://{DB_HOST}:3306/{DB_NAME}?allowPublicKeyRetrieval=true&useSSL=false"

    properties = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    print("Writing data to MySQL via JDBC...")
    # Bulk write to MySQL in parallel mode
    df_transformed.write\
        .mode("append")\
        .jdbc(url=jdbc_url, table="coffee_sales_parkroad", properties=properties)

    print("PySpark ETL complete successfully")
    spark.stop()


if __name__ == "__main__":
        main()
    