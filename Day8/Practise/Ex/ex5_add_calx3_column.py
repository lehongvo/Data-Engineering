# Exercise 5: Add new column calX3 = Forecasted Monthly Revenue * 3 with PySpark
# Show the first 5 rows with the new column

from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col

# Create SparkSession
spark = SparkSession.builder.appName("AddCalX3Column").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Add new column 'calX3' = Forecasted Monthly Revenue * 3
df_with_calx3 = df.withColumn("calX3", col("Forecasted Monthly Revenue") * 3)

# Show the first 5 rows with the new column
print("First 5 rows with the new column 'calX3':")
df_with_calx3.show(5)

# Stop the SparkSession
spark.stop() 