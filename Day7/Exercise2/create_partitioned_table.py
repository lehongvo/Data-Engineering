#!/usr/bin/env python3

from google.cloud import bigquery
from google.api_core.exceptions import Conflict
import os

"""
This script demonstrates how to create partitioned tables in BigQuery.
It covers the three main types of partitioning:
1. Time-unit column partitioning
2. Ingestion-time partitioning
3. Integer range partitioning
"""

# Set up the BigQuery client
client = bigquery.Client()

# Set your project and dataset information
PROJECT_ID = "unique-axle-457602-n6"  # Replace with your Google Cloud project ID
DATASET_ID = "partitioning_demo"
DATASET_REF = f"{PROJECT_ID}.{DATASET_ID}"

def create_dataset_if_not_exists():
    """Create the dataset if it doesn't exist."""
    dataset_ref = client.dataset(DATASET_ID)
    
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} already exists")
    except:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset = client.create_dataset(dataset)
        print(f"Dataset {DATASET_ID} created")

def create_date_partitioned_table():
    """
    Create a table partitioned by date column.
    This is time-unit column partitioning.
    """
    table_id = f"{DATASET_REF}.sales_by_date"
    
    schema = [
        bigquery.SchemaField("transaction_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("transaction_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("product_id", "STRING"),
        bigquery.SchemaField("amount", "FLOAT"),
        bigquery.SchemaField("customer_id", "STRING"),
    ]
    
    table = bigquery.Table(table_id, schema=schema)
    
    # Configure the partition
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="transaction_date"  # The column to use for partitioning
    )
    
    # Add clustering for additional performance
    table.clustering_fields = ["product_id", "customer_id"]
    
    try:
        table = client.create_table(table)
        print(f"Created table {table_id}, partitioned by transaction_date")
    except Conflict:
        print(f"Table {table_id} already exists")

def create_timestamp_partitioned_table():
    """
    Create a table partitioned by timestamp column.
    This is time-unit column partitioning with a finer granularity.
    """
    table_id = f"{DATASET_REF}.events_by_hour"
    
    schema = [
        bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("event_timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("event_type", "STRING"),
        bigquery.SchemaField("user_id", "STRING"),
        bigquery.SchemaField("device", "STRING"),
    ]
    
    table = bigquery.Table(table_id, schema=schema)
    
    # Configure the partition by hour
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.HOUR,
        field="event_timestamp"
    )
    
    # Add clustering for additional performance
    table.clustering_fields = ["event_type", "user_id"]
    
    try:
        table = client.create_table(table)
        print(f"Created table {table_id}, partitioned by event_timestamp (hourly)")
    except Conflict:
        print(f"Table {table_id} already exists")

def create_ingestion_time_partitioned_table():
    """
    Create a table partitioned by ingestion time.
    The partitioning happens automatically based on when data is loaded.
    """
    table_id = f"{DATASET_REF}.logs_by_ingestion"
    
    schema = [
        bigquery.SchemaField("log_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("log_message", "STRING"),
        bigquery.SchemaField("severity", "STRING"),
        bigquery.SchemaField("source", "STRING"),
    ]
    
    table = bigquery.Table(table_id, schema=schema)
    
    # Configure ingestion-time partitioning (no field needed)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY
    )
    
    try:
        table = client.create_table(table)
        print(f"Created table {table_id}, partitioned by ingestion time")
    except Conflict:
        print(f"Table {table_id} already exists")

def create_integer_range_partitioned_table():
    """
    Create a table partitioned by integer range.
    This is useful for non-time-based partitioning.
    """
    table_id = f"{DATASET_REF}.customers_by_age"
    
    schema = [
        bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("city", "STRING"),
        bigquery.SchemaField("signup_date", "DATE"),
    ]
    
    table = bigquery.Table(table_id, schema=schema)
    
    # Configure integer range partitioning
    table.range_partitioning = bigquery.RangePartitioning(
        field="age",
        range_=bigquery.PartitionRange(start=0, end=100, interval=10)
    )
    
    try:
        table = client.create_table(table)
        print(f"Created table {table_id}, partitioned by age range (0-100, interval 10)")
    except Conflict:
        print(f"Table {table_id} already exists")

def main():
    """Main function to create all partitioned tables."""
    print("Creating BigQuery partitioned tables...")
    
    # Create the dataset first
    create_dataset_if_not_exists()
    
    # Create different types of partitioned tables
    create_date_partitioned_table()
    create_timestamp_partitioned_table()
    create_ingestion_time_partitioned_table()
    create_integer_range_partitioned_table()
    
    print("All partitioned tables created successfully!")

if __name__ == "__main__":
    main()