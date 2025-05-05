# Exercise 7: Join two DataFrames with PySpark

from pyspark.sql import SparkSession
from pyspark.sql import Row

# Create SparkSession
spark = SparkSession.builder.appName("JoinDataFrame").getOrCreate()

# Sample data for DataFrame 1
sales_data = [
    (1, "Alice", "US"),
    (2, "Bob", "UK"),
    (3, "Charlie", "US"),
]
sales_columns = ["id", "name", "region"]
df_sales = spark.createDataFrame(sales_data, sales_columns)

# Sample data for DataFrame 2
revenue_data = [
    (1, 1000),
    (2, 1500),
    (4, 2000),
]
revenue_columns = ["id", "revenue"]
df_revenue = spark.createDataFrame(revenue_data, revenue_columns)

# Join two DataFrames on 'id'
df_joined = df_sales.join(df_revenue, on="id", how="inner")

# Show the result
print("Result of joining two DataFrames on 'id':")
df_joined.show()

# Stop the SparkSession
spark.stop() 