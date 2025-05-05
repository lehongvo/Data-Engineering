# Exercise 1: Read CSV data into a DataFrame with PySpark
# Install pyspark if not available: yarn add pyspark (or pip install pyspark if using pip)

from pyspark.sql import SparkSession
import os

# Create SparkSession
spark = SparkSession.builder.appName("ReadCSV").getOrCreate()

# Path to the CSV file (SalesData.csv is located in the csv folder at the same level as Practise)
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
# Assumes the file has a header and infers the schema automatically
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Show the first 5 rows
df.show(5)

# Print the schema of the DataFrame
df.printSchema()

# Stop the SparkSession
spark.stop() 