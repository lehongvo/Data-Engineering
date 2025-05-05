# Exercise 2: View Data Information with PySpark
# Print schema and show the first 5 rows of the DataFrame

from pyspark.sql import SparkSession
import os

# Create SparkSession
spark = SparkSession.builder.appName("ViewDataInfo").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
# Assumes the file has a header and infers the schema automatically
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Print the schema of the DataFrame
print("Schema of the DataFrame:")
df.printSchema()

# Show the first 5 rows
print("First 5 rows of the DataFrame:")
df.show(5)

# Stop the SparkSession
spark.stop() 