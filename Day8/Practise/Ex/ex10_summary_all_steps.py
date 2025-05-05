# Exercise 10: Summary of All Steps on a New Dataset
# This script demonstrates all main steps on a new dataset.
# You can replace 'new_data.csv' with your own file (e.g., from Kaggle).
# Add comments about any errors you encounter and how you fixed them.

from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col, avg, count

# 1. Create SparkSession
spark = SparkSession.builder.appName("SummaryAllSteps").getOrCreate()

# 2. Path to the new CSV file (replace with your own dataset)
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "csv", "new_data.csv"))

# 3. Read the CSV file into a DataFrame
df = None
try:
    df = spark.read.csv(csv_path, header=True, inferSchema=True)
    print("Data loaded successfully!")
except Exception as e:
    print("Error loading data:", e)
    # Ghi chú lỗi và cách khắc phục ở đây
    # Ví dụ: FileNotFoundError -> kiểm tra lại đường dẫn file

if df is not None:
    # 4. Show schema and first 5 rows
    df.printSchema()
    df.show(5)

    # 5. Filter example: filter rows where a column (e.g., 'Region') == 'US'
    if 'Region' in df.columns:
        df_us = df.filter(df.Region == 'US')
        print("First 5 rows where Region is 'US':")
        df_us.show(5)

    # 6. Select specific columns (replace with columns from your dataset)
    selected_columns = df.columns[:5]  # Lấy 5 cột đầu tiên làm ví dụ
    df_selected = df.select(*selected_columns)
    print("First 5 rows with selected columns:")
    df_selected.show(5)

    # 7. Add new column example (replace with your own logic if needed)
    if 'Forecasted Monthly Revenue' in df.columns:
        df_with_calx3 = df.withColumn("calX3", col("Forecasted Monthly Revenue") * 3)
        print("First 5 rows with new column 'calX3':")
        df_with_calx3.show(5)

    # 8. Group by example (replace with columns from your dataset)
    if 'Region' in df.columns and 'Forecasted Monthly Revenue' in df.columns:
        df_grouped = df.groupBy("Region").agg(
            count("Forecasted Monthly Revenue").alias("count"),
            avg("Forecasted Monthly Revenue").alias("avg_Forecasted_Monthly_Revenue")
        )
        print("Count and average Forecasted Monthly Revenue by Region:")
        df_grouped.show()

    # 9. SparkSQL example (register as temp view and run SQL)
    df.createOrReplaceTempView("newdata")
    query = """
        SELECT * FROM newdata LIMIT 5
    """
    result = spark.sql(query)
    print("First 5 rows using SparkSQL:")
    result.show()
else:
    print("DataFrame is not loaded. Please check your data file.")

# 10. Ghi chú lại các lỗi gặp phải và cách khắc phục ở từng bước trên
# (Bạn hãy bổ sung vào file này khi thực hành với dữ liệu thực tế)

# Stop the SparkSession
spark.stop() 