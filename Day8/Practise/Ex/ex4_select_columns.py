# Exercise 4: Select specific columns with PySpark
# Show the first 5 rows with selected columns

from pyspark.sql import SparkSession
import os

# Create SparkSession
spark = SparkSession.builder.appName("SelectColumns").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Select specific columns
selected_columns = [
    "Region",
    "Target Close",
    "Forecasted Monthly Revenue",
    "Opportunity Stage",
    "Latest Status Entry"
]
df_selected = df.select(*selected_columns)

# Show the first 5 rows of the selected columns
print("First 5 rows with selected columns:")
df_selected.show(5)

# Stop the SparkSession
spark.stop() 