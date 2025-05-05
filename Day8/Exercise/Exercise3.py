# Exercise 3: Sales Data Processing with Apache Spark

from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col, sum, row_number, month, desc
from pyspark.sql.window import Window

# Create SparkSession
spark = SparkSession.builder.appName("SalesDataAnalysis").getOrCreate()

# Paths to data files
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.abspath(os.path.join(base_dir, "..", "csv"))

sales_path = os.path.join(csv_dir, "sales.csv")
products_path = os.path.join(csv_dir, "products.csv")
stores_path = os.path.join(csv_dir, "stores.csv")

# Read data into DataFrames
df_sales = spark.read.csv(sales_path, header=True, inferSchema=True)
df_products = spark.read.csv(products_path, header=True, inferSchema=True)
df_stores = spark.read.csv(stores_path, header=True, inferSchema=True)

# 1. Find top 10 best-selling products by region
sales_products = df_sales.join(df_products, "product_id")
sales_products_region = sales_products.join(df_stores, "store_id") \
    .groupBy("region", "product_id", "product_name") \
    .agg(sum("quantity").alias("total_quantity"))

window_region = Window.partitionBy("region").orderBy(desc("total_quantity"))
top10_products_region = sales_products_region.withColumn(
    "rank", row_number().over(window_region)
).filter(col("rank") <= 10)

print("Top 10 best-selling products by region:")
top10_products_region.show(20)

# 2. Analyze revenue trends by month and category
df_sales = df_sales.withColumn("month", month(col("date")))
sales_products_cat = df_sales.join(df_products, "product_id")
revenue_trend = sales_products_cat.groupBy("month", "category") \
    .agg(sum("revenue").alias("total_revenue")) \
    .orderBy("month", "category")

print("Revenue trends by month and category:")
revenue_trend.show(20)

# 3. Identify high and low performing stores
sales_stores = df_sales.join(df_stores, "store_id")
store_performance = sales_stores.groupBy("store_id", "store_name") \
    .agg(sum("revenue").alias("total_revenue")) \
    .orderBy(desc("total_revenue"))

print("Store performance (top 5 highest and lowest):")
store_performance.show(5)
store_performance.orderBy("total_revenue").show(5)

# 4. Save results in Parquet format
output_dir = os.path.join(csv_dir, "output_parquet")
top10_products_region.write.mode("overwrite").parquet(os.path.join(output_dir, "top10_products_region"))
revenue_trend.write.mode("overwrite").parquet(os.path.join(output_dir, "revenue_trend"))
store_performance.write.mode("overwrite").parquet(os.path.join(output_dir, "store_performance"))

print(f"Results have been saved in Parquet format at: {output_dir}")

# Stop SparkSession
spark.stop()
