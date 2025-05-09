#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flink Web Log Analysis
- Lọc các requests lỗi (status code >= 400)
- Tính số lượng truy cập theo URL trong cửa sổ thời gian 10 phút
- Phát hiện các địa chỉ IP có số lượng requests lỗi bất thường
"""

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.window import Tumble
from pyflink.table.expressions import col, lit
from pyflink.table.udf import udf
from pyflink.common.typeinfo import Types
from pyflink.common import Time, Encoder

import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WebLogAnalysis")

def create_input_table(t_env, input_path):
    # Define the input DDL for JSON format
    input_ddl = f"""
        CREATE TABLE web_logs (
            ip STRING,
            url STRING,
            timestamp STRING,
            status_code INT,
            event_time AS TO_TIMESTAMP(timestamp, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_time AS event_time - INTERVAL '5' SECONDS
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{input_path}',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true'
        )
    """
    t_env.execute_sql(input_ddl)
    return t_env.from_path("web_logs")

def create_output_tables(t_env, output_path):
    # Table for error requests
    error_requests_ddl = f"""
        CREATE TABLE error_requests (
            ip STRING,
            url STRING,
            timestamp STRING,
            status_code INT
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{output_path}/error_requests',
            'format' = 'json'
        )
    """
    
    # Table for URL access counts in 10-minute windows
    url_counts_ddl = f"""
        CREATE TABLE url_counts (
            url STRING,
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            access_count BIGINT
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{output_path}/url_counts',
            'format' = 'json'
        )
    """
    
    # Table for abnormal IP detection
    abnormal_ips_ddl = f"""
        CREATE TABLE abnormal_ips (
            ip STRING,
            error_count BIGINT,
            detection_time TIMESTAMP(3)
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{output_path}/abnormal_ips',
            'format' = 'json'
        )
    """
    
    t_env.execute_sql(error_requests_ddl)
    t_env.execute_sql(url_counts_ddl)
    t_env.execute_sql(abnormal_ips_ddl)

def main():
    # Create execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # Set time characteristic
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    env.set_parallelism(1)  # For easier debugging
    
    # Create a Table environment
    settings = EnvironmentSettings.new_instance() \
        .in_streaming_mode() \
        .build()
    
    t_env = StreamTableEnvironment.create(env, settings)
    
    # Set input and output paths
    input_path = "/data/web_logs.json"
    output_path = "/data/output"
    
    # Clean output directory if it exists
    try:
        os.makedirs(output_path, exist_ok=True)
    except Exception as e:
        logger.warning(f"Warning when creating output directory: {e}")
    
    # Create tables
    logger.info("Creating tables...")
    input_table = create_input_table(t_env, input_path)
    create_output_tables(t_env, output_path)
    
    # Register the table
    t_env.create_temporary_view("web_logs", input_table)
    
    # 1. Filter error requests (status code >= 400)
    logger.info("Filtering error requests...")
    error_requests_sql = """
        INSERT INTO error_requests
        SELECT ip, url, timestamp, status_code
        FROM web_logs
        WHERE status_code >= 400
    """
    
    # 2. Calculate URL access counts in 10-minute windows
    logger.info("Calculating URL access counts in 10-minute windows...")
    url_count_sql = """
        INSERT INTO url_counts
        SELECT 
            url,
            window_start,
            window_end,
            COUNT(*) AS access_count
        FROM TABLE(
            TUMBLE(TABLE web_logs, DESCRIPTOR(event_time), INTERVAL '10' MINUTES))
        GROUP BY url, window_start, window_end
    """
    
    # 3. Detect abnormal IPs (those with error count > 5 in a 10-minute window)
    logger.info("Detecting abnormal IPs...")
    abnormal_ips_sql = """
        INSERT INTO abnormal_ips
        SELECT 
            ip,
            COUNT(*) AS error_count,
            MAX(event_time) AS detection_time
        FROM web_logs
        WHERE status_code >= 400
        GROUP BY ip
        HAVING COUNT(*) > 5
    """
    
    # Execute the queries
    logger.info("Executing Flink SQL jobs...")
    error_job = t_env.execute_sql(error_requests_sql)
    url_job = t_env.execute_sql(url_count_sql)
    ip_job = t_env.execute_sql(abnormal_ips_sql)
    
    # Wait for jobs to complete
    error_job.wait()
    url_job.wait()
    ip_job.wait()
    
    logger.info("Job executed successfully!")
    logger.info(f"Results are stored in {output_path} directory.")

if __name__ == "__main__":
    main() 