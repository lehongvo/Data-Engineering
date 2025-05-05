# Exercise 8: Rename and drop columns with PySpark
# Rename 'Latest Status Entry' to 'Latest Status Entry Point' and show the first 5 rows

from pyspark.sql import SparkSession
import os

# Create SparkSession
spark = SparkSession.builder.appName("RenameDropColumn").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Rename column 'Latest Status Entry' to 'Latest Status Entry Point'
df_renamed = df.withColumnRenamed("Latest Status Entry", "Latest Status Entry Point")

# Show the first 5 rows with the renamed column
print("First 5 rows with 'Latest Status Entry' renamed to 'Latest Status Entry Point':")
df_renamed.show(5)

# Stop the SparkSession
spark.stop() 