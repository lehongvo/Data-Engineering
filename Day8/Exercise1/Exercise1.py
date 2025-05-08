# Exercise 1: Load CSV, filter data, and perform basic transformations with PySpark

from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import avg, count

# Create SparkSession
spark = SparkSession.builder.appName("Exercise1").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Show schema and first 5 rows
print("Schema:")
df.printSchema()
print("First 5 rows:")
df.show(5)

# Filter: Only rows where Region is 'US'
df_us = df.filter(df.Region == 'US')
print("Rows where Region is 'US':")
df_us.show()

# Group by Opportunity Stage and calculate count and average Forecasted Monthly Revenue
df_grouped = df.groupBy("Opportunity Stage").agg(
    count("Forecasted Monthly Revenue").alias("count"),
    avg("Forecasted Monthly Revenue").alias("avg_Forecasted_Monthly_Revenue")
)
print("Count and average Forecasted Monthly Revenue by Opportunity Stage:")
df_grouped.show()

# Stop the SparkSession
spark.stop() 