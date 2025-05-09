#!/usr/bin/env python3
"""
Simple Flink processor using Table API to read from Kafka and write results to files
which will be uploaded to BigQuery
"""
import os
import json
import logging
import sys
import time
from datetime import datetime
import traceback

# Set up log directory
LOG_DIR = "/data/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "flink_processor.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("FlinkProcessor")
logger.info(f"Logging to file: {LOG_FILE}")

# Import PyFlink modules
try:
    from pyflink.table import (
        EnvironmentSettings, TableEnvironment
    )
    from pyflink.table.catalog import HiveCatalog
    # Import streaming components as alternative if needed
    try:
        from pyflink.datastream import StreamExecutionEnvironment
        from pyflink.table import StreamTableEnvironment
        logger.info("Successfully imported PyFlink Stream API modules")
    except Exception as e:
        logger.warning(f"Could not import Stream API modules: {e}")
        
    logger.info("Successfully imported PyFlink Table API modules")
except Exception as e:
    logger.error(f"Error importing PyFlink modules: {e}")
    logger.error(traceback.format_exc())
    raise

def create_result_directory():
    """Create directory for result files"""
    results_dir = "/data/results"
    os.makedirs(results_dir, exist_ok=True)
    # Clear previous results if any
    for file in os.listdir(results_dir):
        if file.endswith('.json'):
            os.remove(os.path.join(results_dir, file))
    logger.info(f"Created and cleaned results directory: {results_dir}")
    return results_dir

def create_and_use_table_environment():
    """Create and return a Table Environment"""
    try:
        # Create Table Environment with streaming settings
        logger.info("Creating Table Environment")
        
        # Try first approach with pure TableEnvironment
        try:
            env_settings = EnvironmentSettings.in_streaming_mode()
            t_env = TableEnvironment.create(env_settings)
            logger.info("Created TableEnvironment using in_streaming_mode")
        except Exception as e:
            # If failed, try alternative approach with StreamExecutionEnvironment
            logger.warning(f"Failed to create TableEnvironment directly: {e}, trying alternative method")
            env = StreamExecutionEnvironment.get_execution_environment()
            t_env = StreamTableEnvironment.create(env)
            logger.info("Created StreamTableEnvironment as fallback")
        
        # Configure checkpointing
        t_env.get_config().set_local_timezone("UTC")
        
        logger.info("Table Environment created successfully")
        return t_env
    except Exception as e:
        logger.error(f"Error creating Table Environment: {e}")
        logger.error(traceback.format_exc())
        raise

def create_kafka_source_table(t_env):
    """Create a Kafka source table"""
    try:
        logger.info("Creating Kafka source table")
        
        # Define source DDL
        source_ddl = """
        CREATE TABLE clickstream_source (
            event_id STRING,
            user_id STRING,
            page STRING,
            action STRING,
            device STRING,
            timestamp STRING,
            session_duration INT,
            referrer STRING,
            proctime AS PROCTIME()
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'clickstream',
            'properties.bootstrap.servers' = 'e1-kafka:9092',
            'properties.group.id' = 'flink-consumer-group',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        )
        """
        
        # Execute the DDL
        t_env.execute_sql(source_ddl)
        logger.info("Kafka source table created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating Kafka source table: {e}")
        logger.error(traceback.format_exc())
        return False

def create_file_sink_table(t_env, results_dir):
    """Create a file sink table"""
    try:
        logger.info(f"Creating file sink table with path: {results_dir}")
        
        # Define sink DDL - Make sure path has correct format with file:// prefix
        sink_ddl = f"""
        CREATE TABLE clickstream_aggregated (
            user_id STRING,
            page STRING,
            view_count BIGINT,
            avg_session_duration DOUBLE,
            last_activity STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file://{results_dir}',
            'format' = 'json',
            'sink.rolling-policy.file-size' = '1MB',
            'sink.rolling-policy.rollover-interval' = '60s'
        )
        """
        
        # Execute the DDL
        t_env.execute_sql(sink_ddl)
        logger.info("File sink table created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating file sink table: {e}")
        logger.error(traceback.format_exc())
        return False

def process_clickstream_data(t_env):
    """Process clickstream data and aggregate by user and page"""
    try:
        logger.info("Processing clickstream data")
        
        # Define the SQL query for processing
        query = """
        INSERT INTO clickstream_aggregated
        SELECT 
            user_id,
            page,
            COUNT(*) as view_count,
            AVG(session_duration) as avg_session_duration,
            MAX(timestamp) as last_activity
        FROM clickstream_source
        GROUP BY user_id, page
        """
        
        # Execute the query as a job
        job = t_env.execute_sql(query)
        job_id = job.get_job_id()
        logger.info(f"Started clickstream processing job with ID: {job_id}")
        
        # Get the job client to track job status
        return job, job_id
    except Exception as e:
        logger.error(f"Error processing clickstream data: {e}")
        logger.error(traceback.format_exc())
        return None, None

def upload_results_to_bigquery():
    """Upload result files to BigQuery"""
    try:
        # Import BigQuery modules
        from google.cloud import bigquery
        
        logger.info("Setting up BigQuery client")
        
        # Set up credentials
        credentials_path = '/opt/flink/config/account_key.json'
        if not os.path.exists(credentials_path):
            logger.error(f"Credentials file not found at {credentials_path}")
            return False
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        # Set up BigQuery client
        client = bigquery.Client()
        logger.info("BigQuery client created successfully")
        
        # Configuration for BigQuery
        project_id = "unique-axle-457602-n6"
        dataset_id = "clickstream_analytics"
        table_id = "user_page_stats"
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        
        # Scan results directory for files
        results_dir = "/data/results"
        result_files = []
        for root, _, files in os.walk(results_dir):
            for file in files:
                if file.endswith('.json'):
                    result_files.append(os.path.join(root, file))
        
        # Also check for any legacy files in the /data directory for migration
        data_dir = "/data"
        for file in os.listdir(data_dir):
            if file.startswith('results_') and file.endswith('.json'):
                # Move these files to the results directory
                src_path = os.path.join(data_dir, file)
                dst_path = os.path.join(results_dir, file)
                logger.info(f"Moving legacy result file from {src_path} to {dst_path}")
                try:
                    os.rename(src_path, dst_path)
                    result_files.append(dst_path)
                except Exception as e:
                    logger.error(f"Error moving file {src_path}: {e}")
        
        logger.info(f"Found {len(result_files)} result files")
        
        # Process each result file
        for file_path in result_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                # Insert data into BigQuery
                errors = client.insert_rows_json(table_ref, [data])
                if errors:
                    logger.error(f"Error inserting data from {file_path}: {errors}")
                else:
                    logger.info(f"Successfully uploaded data from {file_path} to BigQuery")
                    
                    # Optionally rename the file to avoid re-uploading
                    processed_path = file_path + ".processed"
                    os.rename(file_path, processed_path)
                    
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                logger.error(traceback.format_exc())
        
        return True
    except Exception as e:
        logger.error(f"Error uploading results to BigQuery: {e}")
        logger.error(traceback.format_exc())
        return False

def main():
    """Main entry point for the Flink processor"""
    try:
        # Create result directory
        results_dir = create_result_directory()
        
        # Create and configure Table Environment
        t_env = create_and_use_table_environment()
        
        # Create tables
        if not create_kafka_source_table(t_env):
            logger.error("Failed to create Kafka source table")
            return
        
        if not create_file_sink_table(t_env, results_dir):
            logger.error("Failed to create file sink table")
            return
        
        # Process data
        job, job_id = process_clickstream_data(t_env)
        if not job:
            logger.error("Failed to start processing job")
            return
        
        # Monitor the job and periodically upload results to BigQuery
        logger.info("Starting job monitoring and BigQuery upload loop")
        
        try:
            upload_interval = 60  # seconds
            last_upload_time = time.time()
            
            while True:
                # Check current time
                current_time = time.time()
                
                # Upload to BigQuery at regular intervals
                if current_time - last_upload_time >= upload_interval:
                    logger.info("Uploading results to BigQuery")
                    upload_results_to_bigquery()
                    last_upload_time = current_time
                
                # Sleep to avoid busy waiting
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Process interrupted by user")
            # One final upload
            upload_results_to_bigquery()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error running Flink job: {e}")
        logger.error(traceback.format_exc()) 