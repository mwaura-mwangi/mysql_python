# Kaggle Coffee Sales ETL & MySQL Analytics

A lightweight Python based ETL (Extract, Transform, Load) pipeline that ingests multi file Kaggle sales data, normalizes schemas and populates a local MySQL database for analytical querying.


## Overview

This project automates the process of combining segmented coffee shop transaction records, handling schema variations across separate source files and bulk loading clean data into MySQL.

### Key Features
* **Schema Alignment:** Automatically handles missing attributes (e.g., missing card transaction columns across files) and aligns column structures.
* **Bulk Insertion:** Utilizes `executemany` with batch operations for performant MySQL data ingestion.
* **Data Sanitization:** Replaces Pandas `NaN` values with native Python `None` types to ensure clean MySQL `NULL` handling.
* **Environment Security:** Manages database credentials safely using environment variables (`.env`).

---

## Tech Stack & Tools

* **Language:** Python 3.12+
* **Environment & Package Management:** `uv`
* **Data Manipulation:** `pandas`
* **Database:** MySQL
* **Database Connector:** `mysql-connector-python`
* **Configuration:** `python-dotenv`

---

## Repository Structure

```text
├── coffee_sales_1.csv       # Source dataset (part 1)
├── coffee_sales_2.csv       # Source dataset (part 2)
├── import_data.py           # Core ETL script (Extract, Transform, Load)
├── main.py                  # test db connection
├── .env                     # Template for local database credentials
├── .gitignore               # Ignores virtual environments & secret .env file
└── README.md                # Project documentation
```
---

## Clone repository

git clone 
cd mysql_python_practice

## Environment setup

uv venv

source .venv/bin/activate

uv pip install -r requirements.txt

## Configure credentials

**DB_HOST**=localhost

**DB_USER**=your_mysql_username

**DB_PASSWORD**=your_mysql_password

## Running the pipeline
uv run import_data.py

## What happens on execution

* Loads coffee_sales_1.csv and coffee_sales_2.csv.

* Adds missing card columns to files where card payments were not originally logged.

* Concatenates datasets into a single unified DataFrame.

* Programmatically creates the coffee_shop database and coffee_sales table if they do not exist.

* Bulk inserts all records and safely closes the database connection.


## Database schema
```
CREATE TABLE IF NOT EXISTS coffee_sales (

    id INT AUTO_INCREMENT PRIMARY KEY,

    sale_date DATE NOT NULL,

    sale_datetime DATETIME NOT NULL,

    cash_type VARCHAR(20) NOT NULL,

    card_number VARCHAR(50) DEFAULT NULL,

    money DECIMAL(10, 2) NOT NULL,

    coffee_name VARCHAR(100) NOT NULL
);
```

---
---
---



# Coffee Sales ETL: PySpark & MySQL Pipeline (Parkroad Branch)

A lightweight ETL pipeline built with PySpark and MySQL to ingest, normalize, and merge multi-batch coffee shop sales records.

This project handles common real world data issues such as schema mismatches between CSV exports and loads clean, typed records into MySQL via JDBC.

---

## What This Pipeline Does

1. **Auto Prepares Infrastructure:** Connects via `mysql-connector-python` to verify and build the target database (`coffee_shop_parkroad`) and strict SQL schema prior to Spark operations.
2. **Handles Schema Drift:** Automatically detects missing columns across batches (e.g., absent `card` column in batch 2) and backfills them with `NULL` before merging.
3. **Normalizes & Type-Casts:** Unifies disparate CSV fields, renames keys to align with SQL conventions, and enforces strict SQL types (`DATE`, `DATETIME`, `DECIMAL(10,2)`).
4. **Parallel JDBC Bulk Load:** Leverages PySpark's distributed `DataFrameWriter` to stream records into MySQL using the MySQL Connector/J driver.

---
## Tech Stack & Tooling
**Language**: Python 3.12+

**Package Management**: uv

**Core Processing Engine**: Apache Spark / PySpark 3.5+

**Database**: MySQL Server

**Drivers & Libraries**: mysql-connector-j (JDBC), mysql-connector-python, python-dotenv


## Environment & Dependencies
uv venv

source .venv/bin/activate

uv pip install pyspark mysql-connector-python python-dotenv

---
## Project Structure

```text
├── coffee_sales_1.csv       # Source dataset (part 1)
├── coffee_sales_2.csv       # Source dataset (part 2)
├── import_data_spark.py     # Core pyspark ETL script (Extract, Transform, Load)
├── main.py                  # test db connection
├── .env                     # Template for local database credentials
├── .gitignore               # Ignores virtual environments & secret .env file
└── README.md                # Project documentation
```

## SQL Verification & Analysis
Once loaded, inspect the transformed records directly in MySQL:

```
USE coffee_shop_parkroad;

# Verify total row count
SELECT COUNT(*) FROM coffee_sales_parkroad;

# Revenue breakdown by coffee product
SELECT 
    coffee_name, 
    COUNT(*) AS total_orders, 
    SUM(money) AS total_revenue
FROM coffee_sales_parkroad
GROUP BY coffee_name
ORDER BY total_revenue DESC;
```