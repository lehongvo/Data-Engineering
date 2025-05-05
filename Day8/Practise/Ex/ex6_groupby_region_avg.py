# Exercise 6: Group by Region and calculate count and average Forecasted Monthly Revenue with PySpark

from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import avg, count

# Create SparkSession
spark = SparkSession.builder.appName("GroupByRegionAvg").getOrCreate()

# Path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "SalesData.csv"))

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Group by Region and calculate count and average Forecasted Monthly Revenue
df_grouped = df.groupBy("Region").agg(
    count("Forecasted Monthly Revenue").alias("count"),
    avg("Forecasted Monthly Revenue").alias("avg_Forecasted_Monthly_Revenue")
)

# Show the result
print("Count and average Forecasted Monthly Revenue by Region:")
df_grouped.show()

# Stop the SparkSession
spark.stop() 