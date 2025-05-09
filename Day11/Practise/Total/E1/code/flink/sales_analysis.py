#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flink application for sales data analysis
- Calculates total revenue by product category per hour
- Used for performance comparison with Kafka Streams
"""

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.window import Tumble
from pyflink.table.expressions import col, lit
from pyflink.common import Time, Types

import json
import os
import logging
import time
import argparse
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FlinkSalesAnalysis")

def create_input_table(t_env, input_path):
    """Create the input table from sales data file."""
    input_ddl = f"""
        CREATE TABLE sales_data (
            sale_id STRING,
            customer_id STRING,
            timestamp STRING,
            location STRING,
            product_category STRING,
            product_name STRING,
            price DOUBLE,
            quantity INT,
            total_amount DOUBLE,
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
    return t_env.from_path("sales_data")

def create_output_table(t_env, output_path):
    """Create the output table for hourly revenue by category."""
    output_ddl = f"""
        CREATE TABLE hourly_revenue (
            product_category STRING,
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            total_revenue DOUBLE
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{output_path}',
            'format' = 'json'
        )
    """
    t_env.execute_sql(output_ddl)

def main():
    """Main function to run the Flink sales analysis."""
    parser = argparse.ArgumentParser(description='Flink Sales Data Analysis')
    parser.add_argument('--input', type=str, default='/data/sales_data.json', 
                        help='Input file path')
    parser.add_argument('--output', type=str, default='/data/output/flink', 
                        help='Output directory path')
    parser.add_argument('--parallelism', type=int, default=1, 
                        help='Parallelism level for Flink execution')
    
    args = parser.parse_args()
    
    # Create execution environment
    start_time = time.time()
    logger.info("Starting Flink Sales Analysis")
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    env.set_parallelism(args.parallelism)
    
    # Create a Table environment
    settings = EnvironmentSettings.new_instance() \
        .in_streaming_mode() \
        .build()
    
    t_env = StreamTableEnvironment.create(env, settings)
    
    # Clean output directory if it exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Create tables
    logger.info("Creating input and output tables...")
    input_table = create_input_table(t_env, args.input)
    create_output_table(t_env, args.output)
    
    # Register the table
    t_env.create_temporary_view("sales_data", input_table)
    
    # Calculate hourly revenue by product category
    logger.info("Calculating hourly revenue by product category...")
    hourly_revenue_sql = """
        INSERT INTO hourly_revenue
        SELECT 
            product_category,
            window_start,
            window_end,
            SUM(total_amount) AS total_revenue
        FROM TABLE(
            TUMBLE(TABLE sales_data, DESCRIPTOR(event_time), INTERVAL '1' HOUR))
        GROUP BY product_category, window_start, window_end
    """
    
    # Execute the query
    logger.info("Executing Flink SQL job...")
    result_job = t_env.execute_sql(hourly_revenue_sql)
    
    # Wait for job to complete
    result_job.wait()
    
    # Calculate and print execution time
    execution_time = time.time() - start_time
    logger.info(f"Job executed successfully in {execution_time:.2f} seconds!")
    logger.info(f"Results are stored in {args.output} directory.")
    
    # Write performance metrics to file
    metrics_file = os.path.join(os.path.dirname(args.output), "flink_metrics.json")
    metrics = {
        "framework": "Apache Flink",
        "execution_time_seconds": execution_time,
        "parallelism": args.parallelism,
        "input_file": args.input,
        "output_directory": args.output
    }
    
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logger.info(f"Performance metrics saved to {metrics_file}")
    
    return execution_time

if __name__ == "__main__":
    main() 