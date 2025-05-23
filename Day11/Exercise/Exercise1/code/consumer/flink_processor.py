#!/usr/bin/env python3
"""
Simple Flink processor using Table API to read from Kafka and write results to files
which will be uploaded to BigQuery.
"""
import os
import json
import logging
import sys
import time
from datetime import datetime
import traceback
from kafka import KafkaConsumer
import uuid
from collections import defaultdict
import threading
import random

# Set up log directory
LOG_DIR = "/data/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "flink_processor.log")
BQ_LOG_FILE = os.path.join(LOG_DIR, "bigquery.log")

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

# Configure BigQuery logging
bq_logger = logging.getLogger("BigQueryUploader")
bq_handler = logging.FileHandler(BQ_LOG_FILE)
bq_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)d] - %(message)s'))
bq_logger.addHandler(bq_handler)
bq_logger.addHandler(logging.StreamHandler(sys.stdout))
bq_logger.setLevel(logging.INFO)
bq_logger.info(f"BigQuery logging to file: {BQ_LOG_FILE}")

# Import PyFlink modules
try:
    # First try to import from the standard location
    from pyflink.table import (
        EnvironmentSettings, TableEnvironment, DataTypes
    )
    from pyflink.table.catalog import HiveCatalog
    from pyflink.table.udf import udf
    
    # Log versions for debugging
    logger.info(f"Python version: {sys.version}")
    logger.info(f"PyFlink is available")
    
    # Import streaming components
    try:
        from pyflink.datastream import StreamExecutionEnvironment, CheckpointingMode
        from pyflink.table import StreamTableEnvironment
        logger.info("Successfully imported PyFlink Stream API modules")
    except Exception as e:
        logger.warning(f"Could not import Stream API modules: {e}")
        
    logger.info("Successfully imported PyFlink Table API modules")
    PYFLINK_AVAILABLE = True
except Exception as e:
    # If the first import fails, try using the classpath from Flink's lib directory
    logger.warning(f"Error importing PyFlink modules the standard way: {e}")
    logger.warning("Will try alternative import method")
    try:
        import sys
        import os
        # Add Flink lib and opt directories to Python path
        flink_lib_dir = "/opt/flink/lib"
        flink_opt_dir = "/opt/flink/opt"
        if flink_lib_dir not in sys.path:
            sys.path.append(flink_lib_dir)
        if flink_opt_dir not in sys.path:
            sys.path.append(flink_opt_dir)
            
        # Try importing again
        from pyflink.table import (
            EnvironmentSettings, TableEnvironment, DataTypes
        )
        from pyflink.table.catalog import HiveCatalog
        from pyflink.table.udf import udf
        
        # Import streaming components
        from pyflink.datastream import StreamExecutionEnvironment, CheckpointingMode
        from pyflink.table import StreamTableEnvironment
        
        logger.info("Successfully imported PyFlink using alternative method")
        PYFLINK_AVAILABLE = True
    except Exception as e:
        logger.error(f"Failed to import PyFlink modules with alternative method: {e}")
        logger.error(traceback.format_exc())
        logger.error("PyFlink is required for this application to run")
        PYFLINK_AVAILABLE = False

def create_result_directory():
    """Create directory for result files"""
    results_dir = "/data/results"
    os.makedirs(results_dir, exist_ok=True)
    # Clear previous results if any
    for file in os.listdir(results_dir):
        if file.endswith('.json'):
            os.remove(os.path.join(results_dir, file))
    # Set permissions to ensure both container and host can access
    os.chmod(results_dir, 0o777)
    logger.info(f"Created and cleaned results directory: {results_dir}")
    return results_dir

def create_and_use_table_environment():
    """Create and return a Table Environment"""
    if not PYFLINK_AVAILABLE:
        raise RuntimeError("PyFlink is not available")
        
    try:
        # Create Table Environment with streaming settings
        logger.info("Creating Table Environment")
        
        # Create StreamExecutionEnvironment first
        s_env = StreamExecutionEnvironment.get_execution_environment()
        
        # Configure checkpointing
        s_env.enable_checkpointing(60000)  # 60 seconds
        s_env.get_checkpoint_config().set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)
        s_env.get_checkpoint_config().set_min_pause_between_checkpoints(30000)  # 30 seconds
        s_env.get_checkpoint_config().set_checkpoint_timeout(300000)  # 5 minutes
        s_env.get_checkpoint_config().set_max_concurrent_checkpoints(1)
        
        # Create StreamTableEnvironment
        t_env = StreamTableEnvironment.create(s_env)
        
        # Configure Table Environment
        t_env.get_config().set("parallelism.default", "2")
        t_env.get_config().set("pipeline.time-characteristic", "EventTime")
        t_env.get_config().set("pipeline.auto-watermark-interval", "200")
        t_env.get_config().set("table.exec.mini-batch.enabled", "true")
        t_env.get_config().set("table.exec.mini-batch.allow-latency", "5s")
        t_env.get_config().set("table.exec.mini-batch.size", "5000")
        t_env.get_config().set("local-timezone", "UTC")
        
        logger.info("Table Environment created successfully with configurations")
        return t_env
    except Exception as e:
        logger.error(f"Error creating Table Environment: {e}")
        logger.error(traceback.format_exc())
        raise

def create_kafka_source_table(t_env):
    """Create a Kafka source table"""
    if not PYFLINK_AVAILABLE:
        raise RuntimeError("PyFlink is not available")
        
    try:
        logger.info("Creating Kafka source table")
        
        # Define source DDL with watermark
        source_ddl = """
        CREATE TABLE clickstream_source (
            event_id STRING,
            user_id STRING,
            page STRING,
            action STRING,
            device STRING,
            event_ts TIMESTAMP(3),
            session_duration INT,
            referrer STRING,
            WATERMARK FOR event_ts AS event_ts - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'clickstream',
            'properties.bootstrap.servers' = 'e1-kafka:9092',
            'properties.group.id' = 'flink-consumer-group',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true'
        )
        """
        
        # Execute the DDL with retry mechanism
        max_retries = 3
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                t_env.execute_sql(source_ddl)
                logger.info("Kafka source table created successfully")
                return True
            except Exception as e:
                retry_count += 1
                last_error = e
                logger.warning(f"Failed to create Kafka source table (attempt {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    time.sleep(5)  # Wait before retry
        
        logger.error(f"Failed to create Kafka source table after {max_retries} attempts: {last_error}")
        return False
        
    except Exception as e:
        logger.error(f"Error creating Kafka source table: {e}")
        logger.error(traceback.format_exc())
        return False

def create_file_sink_table(t_env, results_dir):
    """Create a file sink table"""
    if not PYFLINK_AVAILABLE:
        raise RuntimeError("PyFlink is not available")
        
    try:
        logger.info(f"Creating file sink table with path: {results_dir}")
        
        # Define sink DDL with improved configuration
        sink_ddl = f"""
        CREATE TABLE clickstream_aggregated (
            user_id STRING,
            page STRING,
            view_count BIGINT,
            avg_session_duration DOUBLE,
            last_activity STRING,
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3)
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{results_dir}',
            'format' = 'json',
            'json.encode.decimal-as-plain-number' = 'true',
            'sink.rolling-policy.file-size' = '2MB',
            'sink.rolling-policy.rollover-interval' = '120s',
            'sink.rolling-policy.check-interval' = '60s'
        )
        """
        
        # Execute the DDL with retry mechanism
        max_retries = 3
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                t_env.execute_sql(sink_ddl)
                logger.info("File sink table created successfully")
                return True
            except Exception as e:
                retry_count += 1
                last_error = e
                logger.warning(f"Failed to create file sink table (attempt {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    time.sleep(5)  # Wait before retry
        
        logger.error(f"Failed to create file sink table after {max_retries} attempts: {last_error}")
        return False
        
    except Exception as e:
        logger.error(f"Error creating file sink table: {e}")
        logger.error(traceback.format_exc())
        return False

def process_clickstream_data(t_env):
    """Process clickstream data and aggregate by user and page"""
    if not PYFLINK_AVAILABLE:
        raise RuntimeError("PyFlink is not available")
        
    try:
        logger.info("Processing clickstream data")
        
        # Define the SQL query for processing with windowing
        query = """
        INSERT INTO clickstream_aggregated
        SELECT 
            user_id,
            page,
            COUNT(*) as view_count,
            CAST(AVG(session_duration) AS DOUBLE) as avg_session_duration,
            CAST(MAX(event_ts) AS STRING) as last_activity,
            window_start,
            window_end
        FROM TABLE(
            TUMBLE(
                TABLE clickstream_source,
                DESCRIPTOR(event_ts),
                INTERVAL '5' MINUTES
            )
        )
        GROUP BY user_id, page, window_start, window_end
        """
        
        # Execute the query with retry mechanism
        max_retries = 3
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                job = t_env.execute_sql(query)
                logger.info(f"Started clickstream processing job. TableResult: {job}")
                return job, None
            except Exception as e:
                retry_count += 1
                last_error = e
                logger.warning(f"Failed to start processing job (attempt {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    time.sleep(5)  # Wait before retry
        
        logger.error(f"Failed to start processing job after {max_retries} attempts: {last_error}")
        return None, None
        
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
        bq_logger.info("Starting BigQuery upload process")
        
        # Set up credentials
        credentials_path = '/opt/flink/config/account_key.json'
        if not os.path.exists(credentials_path):
            alt_paths = [
                './config/account_key.json',
                '/config/account_key.json',
                '../config/account_key.json'
            ]
            # Try alternative paths
            for alt_path in alt_paths:
                if os.path.exists(alt_path):
                    credentials_path = alt_path
                    bq_logger.info(f"Found credentials at alternative path: {alt_path}")
                    break
            else:
                error_msg = f"Credentials file not found at {credentials_path} or any alternative paths"
                logger.error(error_msg)
                bq_logger.error(error_msg)
                return False
        
        # Validate JSON credentials format
        try:
            with open(credentials_path, 'r') as f:
                cred_content = f.read()
                # Simple validation - just check it parses as JSON
                json.loads(cred_content)
                bq_logger.info("Credentials file validated as valid JSON")
        except Exception as e:
            error_msg = f"Invalid credentials file format: {str(e)}"
            logger.error(error_msg)
            bq_logger.error(error_msg)
            return False
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        bq_logger.info(f"Using credentials from: {credentials_path}")
        
        # Set up BigQuery client with retry mechanism
        max_retries = 3
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                client = bigquery.Client()
                logger.info("BigQuery client created successfully")
                bq_logger.info(f"BigQuery client created successfully with project: {client.project}")
                break
            except Exception as e:
                retry_count += 1
                last_error = e
                error_msg = f"Failed to create BigQuery client (attempt {retry_count}/{max_retries}): {str(e)}"
                logger.warning(error_msg)
                bq_logger.warning(error_msg)
                bq_logger.error(traceback.format_exc())
                if retry_count < max_retries:
                    time.sleep(5)  # Wait before retry
                else:
                    error_msg = f"Failed to create BigQuery client after {max_retries} attempts: {str(last_error)}"
                    logger.error(error_msg)
                    bq_logger.error(error_msg)
                    return False
        
        # Configuration for BigQuery
        project_id = "unique-axle-457602-n6"
        dataset_id = "clickstream_analytics"
        table_id = "user_page_stats"
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        bq_logger.info(f"Target BigQuery table: {table_ref}")
        
        # Scan results directory for files - check multiple possible locations
        result_files = []
        
        # Primary results directory in container
        container_results_dir = "/data/results"
        if os.path.exists(container_results_dir):
            bq_logger.info(f"Checking container results directory: {container_results_dir}")
            for file in os.listdir(container_results_dir):
                if file.endswith('.json') and not file.endswith('.processed.json'):
                    result_files.append(os.path.join(container_results_dir, file))
            bq_logger.info(f"Found {len(result_files)} files in container results directory")
        
        # Alternative path if run from local machine
        local_results_dir = "./data/results"
        if os.path.exists(local_results_dir) and local_results_dir != container_results_dir:
            bq_logger.info(f"Checking local results directory: {local_results_dir}")
            for file in os.listdir(local_results_dir):
                if file.endswith('.json') and not file.endswith('.processed.json'):
                    file_path = os.path.join(local_results_dir, file)
                    if file_path not in result_files:  # Avoid duplicates
                        result_files.append(file_path)
            bq_logger.info(f"Found total of {len(result_files)} files after checking local directory")
        
        # Check root data directory for legacy or misplaced files
        data_dirs = ["/data", "./data"]
        for data_dir in data_dirs:
            if os.path.exists(data_dir):
                bq_logger.info(f"Checking data directory: {data_dir}")
                for file in os.listdir(data_dir):
                    if (file.startswith('results_') or file.startswith('fallback_results_')) and file.endswith('.json'):
                        # Don't move files, just add them to the list to be processed
                        file_path = os.path.join(data_dir, file)
                        if file_path not in result_files:  # Avoid duplicates
                            result_files.append(file_path)
                            bq_logger.info(f"Found result file in data dir: {file_path}")
        
        logger.info(f"Found {len(result_files)} result files to process")
        bq_logger.info(f"Found {len(result_files)} result files to process: {result_files}")
        
        # Process each result file
        for file_path in result_files:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    bq_logger.info(f"Processing file: {file_path}")
                    try:
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                            bq_logger.info(f"File content sample: {file_content[:500]}{'...' if len(file_content) > 500 else ''}")
                            data = json.loads(file_content)
                    except FileNotFoundError:
                        bq_logger.error(f"File not found: {file_path}")
                        # Try with alternative path format if possible
                        if file_path.startswith('/data/'):
                            alt_path = '.' + file_path
                            bq_logger.info(f"Trying alternative path: {alt_path}")
                            with open(alt_path, 'r') as f:
                                file_content = f.read()
                                bq_logger.info(f"File content from alt path: {file_content[:500]}{'...' if len(file_content) > 500 else ''}")
                                data = json.loads(file_content)
                            file_path = alt_path  # Update path for later operations
                        else:
                            raise
                    
                    # Check if data is a list or dict
                    records = data if isinstance(data, list) else [data]
                    bq_logger.info(f"Parsed {len(records)} records from {file_path}")
                        
                    # Insert data into BigQuery
                    bq_logger.info(f"Uploading {len(records)} records to BigQuery table {table_ref}")
                    try:
                        errors = client.insert_rows_json(table_ref, records)
                        if errors:
                            error_msg = f"Error inserting data: {errors}"
                            logger.error(error_msg)
                            bq_logger.error(error_msg)
                            raise Exception(error_msg)
                        
                        logger.info(f"Successfully uploaded data from {file_path} to BigQuery")
                        bq_logger.info(f"Successfully uploaded data from {file_path} to BigQuery")
                    except Exception as e:
                        bq_logger.error(f"BigQuery insert error: {str(e)}")
                        # Dump detailed error info 
                        try:
                            bq_logger.error(f"First record being inserted: {records[0]}")
                        except:
                            pass
                        raise
                    
                    # Delete the file after successful upload
                    try:
                        os.remove(file_path)
                        logger.info(f"Deleted processed file: {file_path}")
                        bq_logger.info(f"Deleted processed file: {file_path}")
                    except Exception as e:
                        bq_logger.warning(f"Could not delete file {file_path}: {str(e)}")
                    break
                    
                except Exception as e:
                    retry_count += 1
                    error_msg = f"Failed to process file {file_path} (attempt {retry_count}/{max_retries}): {str(e)}"
                    logger.warning(error_msg)
                    bq_logger.warning(error_msg)
                    bq_logger.error(traceback.format_exc())
                    if retry_count == max_retries:
                        error_msg = f"Failed to process file {file_path} after {max_retries} attempts"
                        logger.error(error_msg)
                        bq_logger.error(error_msg)
                    else:
                        time.sleep(5)  # Wait before retry
        
        # Clean up any old .processed files that might exist from previous runs
        for directory in [container_results_dir, local_results_dir]:
            if os.path.exists(directory):
                cleanup_processed_files(directory)
        
        return True
    except Exception as e:
        error_msg = f"Error uploading results to BigQuery: {str(e)}"
        logger.error(error_msg)
        bq_logger.error(error_msg)
        bq_logger.error(traceback.format_exc())
        return False

def cleanup_processed_files(directory):
    """Clean up any old processed files"""
    try:
        count = 0
        for filename in os.listdir(directory):
            if filename.endswith('.processed') or filename.endswith('.processed.json'):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
                count += 1
        
        if count > 0:
            logger.info(f"Cleaned up {count} old processed files")
    except Exception as e:
        logger.error(f"Error cleaning up processed files: {e}")
        logger.error(traceback.format_exc())

def monitor_job_metrics(job_id):
    """Monitor Flink job metrics"""
    try:
        # Add monitoring logic here
        pass
    except Exception as e:
        logger.error(f"Error monitoring job metrics: {e}")
        logger.error(traceback.format_exc())

def main():
    """Main entry point for the Flink processor"""
    try:
        # Create result directory
        results_dir = create_result_directory()
        
        # Clean up any old processed files that might exist
        cleanup_processed_files(results_dir)
        
        # Check if PyFlink is available
        if not PYFLINK_AVAILABLE:
            logger.error("PyFlink is not available. Application requires PyFlink to run.")
            logger.error("Please ensure PyFlink is properly installed.")
            # Exit with error code
            return 1
            
        # PyFlink is available, use it
        # Create and configure Table Environment
        t_env = create_and_use_table_environment()
        
        # Create tables
        if not create_kafka_source_table(t_env):
            logger.error("Failed to create Kafka source table")
            return 1
        
        if not create_file_sink_table(t_env, results_dir):
            logger.error("Failed to create file sink table")
            return 1
        
        # Process data
        job, job_id = process_clickstream_data(t_env)
        if not job:
            logger.error("Failed to start processing job")
            return 1
        
        # Monitor the job and periodically upload results to BigQuery
        logger.info("Starting job monitoring and BigQuery upload loop")
        
        try:
            upload_interval = 60  # seconds
            last_upload_time = time.time()
            
            while True:
                current_time = time.time()
                if current_time - last_upload_time >= upload_interval:
                    logger.info("Uploading results to BigQuery")
                    if upload_results_to_bigquery():
                        last_upload_time = current_time
                    else:
                        logger.warning("Failed to upload results, will retry in next interval")
                # Sleep to avoid busy waiting
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Process interrupted by user")
            upload_results_to_bigquery()
            return 0
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code if exit_code is not None else 1)
    except Exception as e:
        logger.error(f"Error running job: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1) 