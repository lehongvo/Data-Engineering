# Exercise 4: ETL Pipeline and Data Warehouse Simulation (extract from PostgreSQL, transform with Spark, load to Parquet/BigQuery)

from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col, count, when

# PostgreSQL config
db_url = "jdbc:postgresql://localhost:5432/sparkdb"
db_properties = {
    "user": "sparkuser",
    "password": "sparkpass",
    "driver": "org.postgresql.Driver"
}

# Set these values according to your Google Cloud configuration
GCP_PROJECT = "unique-axle-457602-n6"
BQ_DATASET = "apache_datatset"  # or dataset you want to use
BQ_TABLE = f"{GCP_PROJECT}.{BQ_DATASET}.fact_sales"
GCS_BUCKET = "unique-axle-457602-n6-temp"  # Bucket for temporary storage

# Create SparkSession (GCS and BigQuery connector configurations are set in run.sh)
spark = SparkSession.builder.appName("ETL_Pipeline_Demo").getOrCreate()

# 1. Extract: Read from PostgreSQL
df_sales = spark.read.jdbc(url=db_url, table="sales", properties=db_properties)
df_products = spark.read.jdbc(url=db_url, table="products", properties=db_properties)
df_stores = spark.read.jdbc(url=db_url, table="stores", properties=db_properties)
print("Extracted data from PostgreSQL.")

# 2. Data Quality Check (null check, can add more)
print("Checking data quality...")
null_sales = df_sales.select([count(when(col(c).isNull(), c)).alias(c) for c in df_sales.columns])
null_sales.show()
if any(null_sales.first()[c] > 0 for c in null_sales.columns):
    print("Warning: Null values found in sales data!")

# 3. Transform: Join and create star schema (fact + dimension tables)
fact_sales = df_sales.join(df_products, "product_id").join(df_stores, "store_id")
fact_sales = fact_sales.select(
    "date", "product_id", "product_name", "category",
    "store_id", "store_name", "region", "quantity", "revenue"
)
print("Transformed data into star schema (fact_sales):")
fact_sales.show(5)

# 4. Load: Save to BigQuery (fallback to Parquet if unsuccessful)
try:
    print("Attempting to upload data to BigQuery...")
    # Check GCS filesystem configuration
    sc = spark.sparkContext
    hadoopConf = sc._jsc.hadoopConfiguration()
    for name in hadoopConf.iterator():
        if "gs" in name.getKey():
            print(f"Hadoop config: {name.getKey()} = {name.getValue()}")
            
    # Upload to BigQuery
    fact_sales.write.format("bigquery") \
        .option("table", BQ_TABLE) \
        .option("temporaryGcsBucket", GCS_BUCKET) \
        .mode("overwrite").save()
    print(f"Fact table loaded to BigQuery: {BQ_TABLE}")
except Exception as e:
    print("Error during BigQuery upload:", e)
    print("Falling back to Parquet storage...")
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "csv", "etl_output_parquet"))
    fact_sales.write.mode("overwrite").parquet(os.path.join(output_dir, "fact_sales"))
    print(f"Fact table saved to Parquet at: {output_dir}/fact_sales")
    print("\nTo successfully upload to BigQuery, the following steps are required:")
    print("1. Ensure GCS connector (gcs-connector-hadoop3-latest.jar) is added to classpath")
    print("2. Ensure service account has access to BigQuery and GCS")
    print("3. Ensure fs.gs.impl and fs.AbstractFileSystem.gs.impl are properly configured")

print("ETL pipeline completed successfully.")

spark.stop()
