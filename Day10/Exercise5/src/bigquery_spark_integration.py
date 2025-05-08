#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import findspark
from datetime import datetime
from pyspark.sql import SparkSession
from google.cloud import bigquery
from google.oauth2 import service_account

# Initialize findspark to locate Spark installation
findspark.init()

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bigquery_spark.log"),
        logging.StreamHandler()
    ]
)

# Setup Spark logging
spark_logger = logging.getLogger("spark-logs")
spark_handler = logging.FileHandler("logs/spark.log")
spark_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
spark_logger.addHandler(spark_handler)
spark_logger.setLevel(logging.INFO)

logger = logging.getLogger("bigquery-spark-integration")

class BigQuerySparkIntegration:
    def __init__(self, project_id, credentials_path, temp_gcs_bucket=None):
        """Initialize BigQuery-Spark Integration."""
        logger.info("Initializing BigQuery-Spark Integration")
        spark_logger.info("Starting Spark session initialization")
        
        # Set Google Cloud credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        # Get credentials
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        
        # Project info
        self.project_id = project_id
        self.temp_gcs_bucket = temp_gcs_bucket
        
        # Initialize BigQuery client
        self.bq_client = bigquery.Client(
            credentials=self.credentials,
            project=self.project_id
        )
        
        # Get the connector JAR path from environment or use default
        connector_jar = os.environ.get('SPARK_CONNECTOR_PATH', None)
        
        # Initialize Spark session
        builder = SparkSession.builder \
            .appName("BigQuerySparkIntegration") \
            .config("spark.sql.warehouse.dir", "spark-warehouse") \
            .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
            .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_path)
        
        # Add the connector JAR if provided
        if connector_jar and os.path.exists(connector_jar):
            logger.info(f"Using BigQuery connector JAR: {connector_jar}")
            spark_logger.info(f"Adding BigQuery connector JAR: {connector_jar}")
            builder = builder.config("spark.jars", connector_jar)
        else:
            logger.warning("BigQuery connector JAR not found. BigQuery operations may fail.")
            spark_logger.warning("BigQuery connector JAR not found. BigQuery operations may fail.")
        
        # Create Spark session
        self.spark = builder.getOrCreate()
        
        # Set log level
        self.spark.sparkContext.setLogLevel("INFO")
        
        logger.info(f"Spark session created with application ID: {self.spark.sparkContext.applicationId}")
        spark_logger.info(f"Spark session created with application ID: {self.spark.sparkContext.applicationId}")
        logger.info(f"Connected to BigQuery Project: {self.project_id}")
        spark_logger.info(f"Connected to BigQuery Project: {self.project_id}")
    
    def extract_from_bigquery(self, query, output_dir=None):
        """Extract data from BigQuery into a Spark DataFrame.
        
        Args:
            query: SQL query to execute in BigQuery
            output_dir: Optional directory to save extracted data as Parquet
            
        Returns:
            PySpark DataFrame with query results
        """
        logger.info("Extracting data from BigQuery")
        logger.info(f"Executing query: {query}")
        
        try:
            # Extract dataset and table name from query
            if query.startswith('(SELECT') and query.endswith(')'):
                # For direct queries, use the read API with a table reference
                table_id = "bigquery-public-data:samples.natality"
                
                logger.info(f"Reading from table: {table_id}")
                
                # Read directly from BigQuery using table ID with a smaller limit
                df = self.spark.read \
                    .format("bigquery") \
                    .option("table", table_id) \
                    .option("filter", "true") \
                    .option("limit", "5000") \
                    .option("credentialsFile", os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')) \
                    .load()
            else:
                logger.info("Using direct table read with specified table ID")
                # Use the provided query as a table ID
                df = self.spark.read \
                    .format("bigquery") \
                    .option("table", query) \
                    .option("credentialsFile", os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')) \
                    .load()
            
            # Display schema and sample data
            logger.info("Data schema:")
            df.printSchema()
            
            logger.info("Sample data:")
            df.show(5, truncate=False)
            
            # Save data locally if requested
            if output_dir:
                save_path = os.path.join(output_dir, f"bq_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                logger.info(f"Saving extracted data to {save_path}")
                df.write.mode("overwrite").parquet(save_path)
            
            return df
            
        except Exception as e:
            logger.error(f"Error extracting data from BigQuery: {e}")
            raise
    
    def write_to_bigquery(self, df, table_id, write_mode="append"):
        """Write Spark DataFrame to BigQuery table.
        
        Args:
            df: Spark DataFrame to write
            table_id: Destination table ID in format 'dataset.table'
            write_mode: Write mode ('append', 'overwrite', 'ignore', 'error')
        """
        logger.info(f"Writing data to BigQuery table {table_id}")
        
        try:
            # Write DataFrame to BigQuery
            df.write \
                .format("bigquery") \
                .option("table", f"{self.project_id}.{table_id}") \
                .option("temporaryGcsBucket", self.temp_gcs_bucket) \
                .mode(write_mode) \
                .save()
            
            logger.info(f"Successfully wrote data to {table_id}")
            
            # Get row count from BigQuery
            query = f"SELECT COUNT(*) as count FROM `{self.project_id}.{table_id}`"
            count_result = self.bq_client.query(query).result()
            count = next(count_result).count
            
            logger.info(f"Table {table_id} now has {count} rows")
            
        except Exception as e:
            logger.error(f"Error writing to BigQuery: {e}")
            raise
    
    def run_spark_sql(self, df, query):
        """Run a Spark SQL query on a DataFrame.
        
        Args:
            df: Input Spark DataFrame
            query: SQL query to execute
            
        Returns:
            Result of the SQL query as a Spark DataFrame
        """
        logger.info(f"Running Spark SQL query: {query}")
        
        try:
            # Register DataFrame as a temp view
            df.createOrReplaceTempView("temp_data")
            
            # Execute the query
            result_df = self.spark.sql(query)
            
            # Show the result
            logger.info("Query result:")
            result_df.show(10)
            
            return result_df
        
        except Exception as e:
            logger.error(f"Error running Spark SQL: {e}")
            raise
    
    def stop(self):
        """Stop Spark session."""
        if self.spark:
            self.spark.stop()
            logger.info("Spark session stopped")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Path to service account key
    credentials_path = "config/account_key.json"
    
    try:
        # Example usage
        project_id = "your-gcp-project-id"  # Replace with your GCP project ID
        
        integration = BigQuerySparkIntegration(
            project_id=project_id,
            credentials_path=credentials_path,
            temp_gcs_bucket="your-temp-bucket"  # Replace with your GCS bucket
        )
        
        # Extract data from BigQuery
        query = "(SELECT * FROM `bigquery-public-data.samples.natality` LIMIT 1000)"
        df = integration.extract_from_bigquery(query, "data")
        
        # Example analysis with Spark SQL
        analysis_query = """
        SELECT year, AVG(weight_pounds) as avg_weight, COUNT(*) as count
        FROM temp_data
        GROUP BY year
        ORDER BY year DESC
        """
        result_df = integration.run_spark_sql(df, analysis_query)
        
        # Write results back to BigQuery
        integration.write_to_bigquery(result_df, "my_dataset.birth_weight_analysis", "overwrite")
        
    except Exception as e:
        logger.error(f"Failed to run BigQuery-Spark integration: {e}")
    finally:
        if 'integration' in locals():
            integration.stop()