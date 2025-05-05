# Exercise 3: Filter data where Region is US with PySpark
# Show the first 5 rows where Region == 'US'

from pyspark.sql import SparkSession
import os

# Create SparkSession
spark = SparkSession.builder.appName("FilterRegionUS").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Filter rows where Region is 'US'
df_us = df.filter(df.Region == 'US')

# Show the first 5 rows of the filtered DataFrame
print("First 5 rows where Region is 'US':")
df_us.show(10)

# Stop the SparkSession
spark.stop() 