# Exercise 2: Save processed Spark data to CSV and load into PostgreSQL

from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col

# Create SparkSession
spark = SparkSession.builder.appName("Exercise2").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Example processing: filter Region == 'US'
df_us = df.filter(col("Region") == 'US')

# Save processed data to a new CSV file
output_csv_path = os.path.abspath(os.path.join(base_dir, "..", "csv", "SalesData_US.csv"))
df_us.write.mode("overwrite").option("header", True).csv(output_csv_path)
print(f"Processed data saved to: {output_csv_path}")

# Load processed data into PostgreSQL
# Config matches docker-compose.yml
# Ensure you have the PostgreSQL JDBC driver available to Spark

db_url = "jdbc:postgresql://localhost:5432/sparkdb"
db_properties = {
    "user": "sparkuser",
    "password": "sparkpass",
    "driver": "org.postgresql.Driver"
}
table_name = "salesdata_us"

# Uncomment the following lines to actually write to PostgreSQL (requires running PostgreSQL and the JDBC driver)
df_us.write.jdbc(url=db_url, table=table_name, mode="overwrite", properties=db_properties)
print(f"Processed data loaded into PostgreSQL table: {table_name}")

# Stop the SparkSession
spark.stop() 