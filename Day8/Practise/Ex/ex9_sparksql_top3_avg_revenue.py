# Exercise 9: SparkSQL - Top 3 Regions by Average Forecasted Monthly Revenue

from pyspark.sql import SparkSession
import os

# Create SparkSession
spark = SparkSession.builder.appName("SparkSQLTop3AvgRevenue").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Register DataFrame as a temporary view
df.createOrReplaceTempView("sales")

# Query: Top 3 Regions by average Forecasted Monthly Revenue
query = """
    SELECT Region, AVG(`Forecasted Monthly Revenue`) AS avg_revenue
    FROM sales
    GROUP BY Region
    ORDER BY avg_revenue DESC
    LIMIT 3
"""
result = spark.sql(query)

print("Top 3 Regions by average Forecasted Monthly Revenue:")
result.show()

# Stop the SparkSession
spark.stop()