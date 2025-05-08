# Exercise 4: ETL Pipeline and Data Warehouse Simulation (extract from PostgreSQL, transform with Spark, load to Parquet/BigQuery)

from pyspark.sql import SparkSession
import os
import logging
import time
import datetime
from pyspark.sql.functions import col, count, when, lit, expr, sum, min, max, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

# Thiết lập logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("etl_pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ETL_Pipeline")

# Class để theo dõi metrics của pipeline
class PipelineMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.stage_metrics = {}
        self.data_quality_metrics = {}
        
    def start_stage(self, stage_name):
        self.stage_metrics[stage_name] = {"start_time": time.time(), "status": "running"}
        logger.info(f"Starting stage: {stage_name}")
        
    def end_stage(self, stage_name, status="success", records=None, error=None):
        if stage_name in self.stage_metrics:
            end_time = time.time()
            duration = end_time - self.stage_metrics[stage_name]["start_time"]
            self.stage_metrics[stage_name].update({
                "end_time": end_time,
                "duration": duration,
                "status": status
            })
            if records is not None:
                self.stage_metrics[stage_name]["records"] = records
            if error is not None:
                self.stage_metrics[stage_name]["error"] = str(error)
                
            logger.info(f"Completed stage: {stage_name}, Status: {status}, Duration: {duration:.2f}s" + 
                       (f", Records: {records}" if records is not None else ""))
    
    def add_data_quality_metric(self, name, value, threshold=None, status="pass"):
        self.data_quality_metrics[name] = {
            "value": value,
            "threshold": threshold,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    def get_summary(self):
        total_duration = time.time() - self.start_time
        successful_stages = sum(1 for stage in self.stage_metrics.values() if stage.get("status") == "success")
        failed_stages = sum(1 for stage in self.stage_metrics.values() if stage.get("status") == "error")
        
        # Fix: Convert generators to numbers to avoid the 'NOT_COLUMN_OR_STR' error
        dq_passed = sum(1 for m in self.data_quality_metrics.values() if m.get("status") == "pass")
        dq_failed = sum(1 for m in self.data_quality_metrics.values() if m.get("status") == "fail")
        
        return {
            "total_duration": total_duration,
            "successful_stages": successful_stages,
            "failed_stages": failed_stages,
            "data_quality_passed": dq_passed,
            "data_quality_failed": dq_failed
        }
        
    def log_summary(self):
        summary = self.get_summary()
        logger.info("=" * 50)
        logger.info("ETL Pipeline Summary:")
        logger.info(f"Total Duration: {summary['total_duration']:.2f}s")
        logger.info(f"Successful Stages: {summary['successful_stages']}")
        logger.info(f"Failed Stages: {summary['failed_stages']}")
        logger.info(f"Data Quality Checks Passed: {summary['data_quality_passed']}")
        logger.info(f"Data Quality Checks Failed: {summary['data_quality_failed']}")
        logger.info("=" * 50)

# Class chuyên cho data quality checks
class DataQualityChecker:
    def __init__(self, metrics):
        self.metrics = metrics
        
    def check_null_values(self, df, column_name, threshold_pct=1.0):
        total_rows = df.count()
        null_count = df.filter(col(column_name).isNull()).count()
        null_percentage = (null_count / total_rows) * 100 if total_rows > 0 else 0
        
        status = "pass" if null_percentage <= threshold_pct else "fail"
        metric_name = f"null_check_{column_name}"
        
        self.metrics.add_data_quality_metric(
            name=metric_name,
            value=null_percentage,
            threshold=threshold_pct,
            status=status
        )
        
        if status == "fail":
            logger.warning(f"Data quality check failed: {column_name} has {null_percentage:.2f}% null values (threshold: {threshold_pct}%)")
        
        return null_percentage <= threshold_pct
    
    def check_duplicate_records(self, df, key_columns):
        total_rows = df.count()
        distinct_rows = df.select(key_columns).distinct().count()
        duplicate_count = total_rows - distinct_rows
        duplicate_percentage = (duplicate_count / total_rows) * 100 if total_rows > 0 else 0
        
        status = "pass" if duplicate_percentage == 0 else "fail"
        key_columns_str = "_".join(key_columns)
        metric_name = f"duplicate_check_{key_columns_str}"
        
        self.metrics.add_data_quality_metric(
            name=metric_name,
            value=duplicate_percentage,
            threshold=0,
            status=status
        )
        
        if status == "fail":
            logger.warning(f"Data quality check failed: Found {duplicate_count} duplicate records ({duplicate_percentage:.2f}%) based on keys: {key_columns}")
        
        return duplicate_percentage == 0
    
    def check_value_range(self, df, column_name, min_value=None, max_value=None):
        if min_value is not None:
            below_min = df.filter(col(column_name) < min_value).count()
            status = "pass" if below_min == 0 else "fail"
            metric_name = f"range_check_{column_name}_min"
            
            self.metrics.add_data_quality_metric(
                name=metric_name,
                value=below_min,
                threshold=0,
                status=status
            )
            
            if status == "fail":
                logger.warning(f"Data quality check failed: {below_min} records have {column_name} below minimum value {min_value}")
        
        if max_value is not None:
            above_max = df.filter(col(column_name) > max_value).count()
            status = "pass" if above_max == 0 else "fail"
            metric_name = f"range_check_{column_name}_max"
            
            self.metrics.add_data_quality_metric(
                name=metric_name,
                value=above_max,
                threshold=0,
                status=status
            )
            
            if status == "fail":
                logger.warning(f"Data quality check failed: {above_max} records have {column_name} above maximum value {max_value}")
        
        return (below_min if min_value is not None else 0) + (above_max if max_value is not None else 0) == 0
    
    def check_column_statistics(self, df, column_name, expected_min=None, expected_max=None, expected_avg=None, tolerance=0.1):
        stats = df.select(
            min(col(column_name)).alias("min"),
            max(col(column_name)).alias("max"),
            avg(col(column_name)).alias("avg")
        ).collect()[0]
        
        all_checks_passed = True
        
        if expected_min is not None:
            min_diff_pct = abs(stats.min - expected_min) / expected_min if expected_min != 0 else abs(stats.min)
            min_status = "pass" if min_diff_pct <= tolerance else "fail"
            self.metrics.add_data_quality_metric(
                name=f"stat_check_{column_name}_min",
                value=stats.min,
                threshold=expected_min,
                status=min_status
            )
            if min_status == "fail":
                logger.warning(f"Data quality check failed: {column_name} minimum value {stats.min} differs from expected {expected_min}")
                all_checks_passed = False
        
        if expected_max is not None:
            max_diff_pct = abs(stats.max - expected_max) / expected_max if expected_max != 0 else abs(stats.max)
            max_status = "pass" if max_diff_pct <= tolerance else "fail"
            self.metrics.add_data_quality_metric(
                name=f"stat_check_{column_name}_max",
                value=stats.max,
                threshold=expected_max,
                status=max_status
            )
            if max_status == "fail":
                logger.warning(f"Data quality check failed: {column_name} maximum value {stats.max} differs from expected {expected_max}")
                all_checks_passed = False
        
        if expected_avg is not None:
            avg_diff_pct = abs(stats.avg - expected_avg) / expected_avg if expected_avg != 0 else abs(stats.avg)
            avg_status = "pass" if avg_diff_pct <= tolerance else "fail"
            self.metrics.add_data_quality_metric(
                name=f"stat_check_{column_name}_avg",
                value=stats.avg,
                threshold=expected_avg,
                status=avg_status
            )
            if avg_status == "fail":
                logger.warning(f"Data quality check failed: {column_name} average value {stats.avg} differs from expected {expected_avg}")
                all_checks_passed = False
        
        return all_checks_passed
    
    def check_completeness(self, df, required_columns):
        missing_columns = [c for c in required_columns if c not in df.columns]
        status = "pass" if len(missing_columns) == 0 else "fail"
        
        self.metrics.add_data_quality_metric(
            name="schema_completeness",
            value=len(missing_columns),
            threshold=0,
            status=status
        )
        
        if status == "fail":
            logger.warning(f"Data quality check failed: Missing required columns: {missing_columns}")
        
        return len(missing_columns) == 0

# PostgreSQL config
db_url = "jdbc:postgresql://localhost:5432/sparkdb"
db_properties = {
    "user": "sparkuser",
    "password": "sparkpass",
    "driver": "org.postgresql.Driver"
}

# Use environment variables if available (higher priority)
import os
if os.environ.get('POSTGRES_HOST'):
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT', '5432')
    db = os.environ.get('POSTGRES_DB', 'sparkdb')
    db_url = f"jdbc:postgresql://{host}:{port}/{db}"
    
    db_properties = {
        "user": os.environ.get('POSTGRES_USER', 'sparkuser'),
        "password": os.environ.get('POSTGRES_PASSWORD', 'sparkpass'),
        "driver": "org.postgresql.Driver"
    }
    
    logger.info(f"Using PostgreSQL connection from environment: {host}:{port}/{db}")
else:
    logger.info("Using default PostgreSQL connection: localhost:5432/sparkdb")

# Set these values according to your Google Cloud configuration
GCP_PROJECT = "unique-axle-457602-n6"
BQ_DATASET = "apache_datatset"  # or dataset you want to use
BQ_TABLE = f"{GCP_PROJECT}.{BQ_DATASET}.fact_sales"
GCS_BUCKET = "unique-axle-457602-n6-temp"  # Bucket for temporary storage

# Hàm tạo mock data khi cần
def create_mock_data(spark):
    """Create mock data for development and testing when database is not available"""
    logger.info("Creating mock data since database connection failed...")
    
    # Định nghĩa schema
    sales_schema = StructType([
        StructField("product_id", IntegerType(), False),
        StructField("store_id", IntegerType(), False),
        StructField("date", StringType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("revenue", DoubleType(), False)
    ])
    
    products_schema = StructType([
        StructField("product_id", IntegerType(), False),
        StructField("product_name", StringType(), False),
        StructField("category", StringType(), False)
    ])
    
    stores_schema = StructType([
        StructField("store_id", IntegerType(), False),
        StructField("store_name", StringType(), False),
        StructField("region", StringType(), False)
    ])
    
    # Dữ liệu mẫu
    sales_data = [
        (1, 1, "2023-01-01", 5, 100.0),
        (2, 1, "2023-01-01", 3, 150.0),
        (3, 2, "2023-01-02", 2, 50.0),
        (1, 2, "2023-01-02", 10, 200.0),
        (2, 3, "2023-01-03", 7, 350.0)
    ]
    
    products_data = [
        (1, "Laptop", "Electronics"),
        (2, "Smartphone", "Electronics"),
        (3, "T-shirt", "Clothing")
    ]
    
    stores_data = [
        (1, "Main Store", "North"),
        (2, "Mall Shop", "South"),
        (3, "Online Store", "Online")
    ]
    
    # Tạo DataFrame
    df_sales = spark.createDataFrame(sales_data, sales_schema)
    df_products = spark.createDataFrame(products_data, products_schema)
    df_stores = spark.createDataFrame(stores_data, stores_schema)
    
    return df_sales, df_products, df_stores

# Create SparkSession (GCS and BigQuery connector configurations are set in run.sh)
spark = SparkSession.builder.appName("ETL_Pipeline_Demo").getOrCreate()

# Khởi tạo hệ thống monitoring
metrics = PipelineMetrics()
data_quality = DataQualityChecker(metrics)

try:
    # 1. Extract: Read from PostgreSQL
    metrics.start_stage("extract_data")
    
    try:
        # Thử kết nối với PostgreSQL
        df_sales = spark.read.jdbc(url=db_url, table="sales", properties=db_properties)
        df_products = spark.read.jdbc(url=db_url, table="products", properties=db_properties)
        df_stores = spark.read.jdbc(url=db_url, table="stores", properties=db_properties)
        
        # Record counts from source
        sales_count = df_sales.count()
        products_count = df_products.count()
        stores_count = df_stores.count()
        
        metrics.end_stage("extract_data", status="success", 
                         records={"sales": sales_count, "products": products_count, "stores": stores_count})
        logger.info(f"Extracted data from PostgreSQL: {sales_count} sales, {products_count} products, {stores_count} stores")
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {str(e)}")
        logger.info("Using mock data instead...")
        
        # Tạo mock data để tiếp tục phát triển
        df_sales, df_products, df_stores = create_mock_data(spark)
        
        # Record counts from mock data
        sales_count = df_sales.count()
        products_count = df_products.count()
        stores_count = df_stores.count()
        
        metrics.end_stage("extract_data", status="success", 
                         records={"sales": sales_count, "products": products_count, "stores": stores_count})
        logger.info(f"Created mock data: {sales_count} sales, {products_count} products, {stores_count} stores")

    # 2. Data Quality Check (kiểm tra chất lượng chuyên nghiệp hơn)
    metrics.start_stage("data_quality_check")
    
    try:
        logger.info("Performing comprehensive data quality checks...")
        
        # Check completeness of schema
        required_sales_columns = ["date", "product_id", "store_id", "quantity", "revenue"]
        schema_complete = data_quality.check_completeness(df_sales, required_sales_columns)
        
        # Check null values for important columns
        null_checks_passed = True
        for column in required_sales_columns:
            null_checks_passed = data_quality.check_null_values(df_sales, column, threshold_pct=5.0) and null_checks_passed
        
        # Check for duplicates
        duplicates_check = data_quality.check_duplicate_records(df_sales, ["date", "product_id", "store_id"])
        
        # Check value ranges
        range_checks_passed = data_quality.check_value_range(df_sales, "quantity", min_value=0)
        range_checks_passed = data_quality.check_value_range(df_sales, "revenue", min_value=0) and range_checks_passed
        
        # Optional: Check referential integrity
        products_integrity = df_sales.join(df_products, "product_id", "left_anti").count() == 0
        stores_integrity = df_sales.join(df_stores, "store_id", "left_anti").count() == 0
        
        if not products_integrity:
            logger.warning("Data quality issue: Some product_id values in sales don't exist in products table")
            metrics.add_data_quality_metric("ref_integrity_products", value=False, status="fail")
        
        if not stores_integrity:
            logger.warning("Data quality issue: Some store_id values in sales don't exist in stores table")
            metrics.add_data_quality_metric("ref_integrity_stores", value=False, status="fail")
        
        # Calculate overall data quality status
        dq_status = "success" if (schema_complete and null_checks_passed and duplicates_check and 
                                range_checks_passed and products_integrity and stores_integrity) else "warning"
        
        metrics.end_stage("data_quality_check", status=dq_status)
    except Exception as e:
        metrics.end_stage("data_quality_check", status="error", error=e)
        logger.error(f"Error during data quality checks: {str(e)}")
        # We continue despite errors in data quality - in production you might want to abort
    
    # 3. Transform: Join and create star schema (fact + dimension tables)
    metrics.start_stage("transform_data")
    
    try:
        fact_sales = df_sales.join(df_products, "product_id").join(df_stores, "store_id")
        fact_sales = fact_sales.select(
            "date", "product_id", "product_name", "category",
            "store_id", "store_name", "region", "quantity", "revenue"
        )
        
        # Add data transformation metrics
        fact_sales_count = fact_sales.count()
        fact_sales_categories = fact_sales.select("category").distinct().count()
        fact_sales_regions = fact_sales.select("region").distinct().count()
        
        transform_metrics = {
            "record_count": fact_sales_count,
            "category_count": fact_sales_categories,
            "region_count": fact_sales_regions
        }
        
        metrics.end_stage("transform_data", status="success", records=transform_metrics)
        logger.info(f"Transformed data into star schema: {fact_sales_count} records across {fact_sales_categories} categories and {fact_sales_regions} regions")
        
        # Log a sample of the transformed data
        logger.info("Sample of transformed fact_sales:")
        fact_sales.show(5)
    except Exception as e:
        metrics.end_stage("transform_data", status="error", error=e)
        logger.error(f"Error during data transformation: {str(e)}")
        raise

    # 4. Load: Save to BigQuery (fallback to Parquet if unsuccessful)
    metrics.start_stage("load_data")
    
    try:
        logger.info("Attempting to upload data to BigQuery...")
        
        # Check GCS filesystem configuration
        sc = spark.sparkContext
        hadoopConf = sc._jsc.hadoopConfiguration()
        hadoop_configs = []
        for name in hadoopConf.iterator():
            if "gs" in name.getKey():
                hadoop_configs.append(f"{name.getKey()} = {name.getValue()}")
                logger.info(f"Hadoop config: {name.getKey()} = {name.getValue()}")
        
        # Upload to BigQuery
        fact_sales.write.format("bigquery") \
            .option("table", BQ_TABLE) \
            .option("temporaryGcsBucket", GCS_BUCKET) \
            .mode("overwrite").save()
        
        metrics.end_stage("load_data", status="success", records=fact_sales_count)
        logger.info(f"Fact table loaded to BigQuery: {BQ_TABLE} ({fact_sales_count} records)")
    except Exception as e:
        logger.warning(f"Error during BigQuery upload: {str(e)}")
        logger.info("Falling back to Parquet storage...")
        
        try:
            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "csv", "etl_output_parquet"))
            fact_sales.write.mode("overwrite").parquet(os.path.join(output_dir, "fact_sales"))
            
            metrics.end_stage("load_data", status="warning", 
                             records={"destination": "parquet", "path": output_dir, "count": fact_sales_count})
            logger.info(f"Fact table saved to Parquet at: {output_dir}/fact_sales ({fact_sales_count} records)")
            
            logger.info("\nTo successfully upload to BigQuery, the following steps are required:")
            logger.info("1. Ensure GCS connector (gcs-connector-hadoop3-latest.jar) is added to classpath")
            logger.info("2. Ensure service account has access to BigQuery and GCS")
            logger.info("3. Ensure fs.gs.impl and fs.AbstractFileSystem.gs.impl are properly configured")
        except Exception as fallback_error:
            metrics.end_stage("load_data", status="error", error=fallback_error)
            logger.error(f"Error during Parquet fallback save: {str(fallback_error)}")
            raise

    # 5. Pipeline Summary & Metrics
    # Xử lý final summary với try-except để tránh generator errors
    try:
        # Tính toán trước các giá trị
        total_duration = time.time() - metrics.start_time
        successful_stages = len([s for s in metrics.stage_metrics.values() if s.get("status") == "success"])
        failed_stages = len([s for s in metrics.stage_metrics.values() if s.get("status") == "error"])
        dq_passed = len([m for m in metrics.data_quality_metrics.values() if m.get("status") == "pass"])
        dq_failed = len([m for m in metrics.data_quality_metrics.values() if m.get("status") == "fail"])
        
        # Log thông tin đã tính
        logger.info("=" * 50)
        logger.info("ETL Pipeline Summary:")
        logger.info(f"Total Duration: {total_duration:.2f}s")
        logger.info(f"Successful Stages: {successful_stages}")
        logger.info(f"Failed Stages: {failed_stages}")
        logger.info(f"Data Quality Checks Passed: {dq_passed}")
        logger.info(f"Data Quality Checks Failed: {dq_failed}")
        logger.info("=" * 50)
        logger.info("ETL pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Error generating summary stats: {str(e)}")
        logger.info("ETL pipeline completed with summary errors.")

except Exception as e:
    logger.error(f"ETL pipeline failed: {str(e)}")
    # In production, you could send alerts, notification, etc.
finally:
    # Clean-up and resource management
    spark.stop()
    logger.info("Spark session stopped. Resources released.")
