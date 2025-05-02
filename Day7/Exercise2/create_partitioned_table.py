#!/usr/bin/env python3

from google.cloud import bigquery
from google.api_core.exceptions import Conflict
import os
from random import randint, choice, uniform
from datetime import datetime, timedelta

try:
    from faker import Faker

    fake = Faker()
except ImportError:
    fake = None

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
        field="transaction_date",  # The column to use for partitioning
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
        type_=bigquery.TimePartitioningType.HOUR, field="event_timestamp"
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
        field="age", range_=bigquery.PartitionRange(start=0, end=100, interval=10)
    )

    try:
        table = client.create_table(table)
        print(
            f"Created table {table_id}, partitioned by age range (0-100, interval 10)"
        )
    except Conflict:
        print(f"Table {table_id} already exists")


def insert_sample_sales_by_date():
    print("Inserting 200 random records into sales_by_date...")
    table_id = f"{DATASET_REF}.sales_by_date"
    rows = []
    base_date = datetime(2025, 1, 1)
    for i in range(200):
        transaction_id = f"TX{i+1:04d}"
        transaction_date = (
            (base_date + timedelta(days=randint(0, 30))).date().isoformat()
        )
        product_id = f"P{randint(1, 20):03d}"
        amount = round(uniform(10, 1000), 2)
        customer_id = f"C{randint(1, 50):03d}"
        rows.append(
            {
                "transaction_id": transaction_id,
                "transaction_date": transaction_date,
                "product_id": product_id,
                "amount": amount,
                "customer_id": customer_id,
            }
        )
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"Errors inserting sales_by_date: {errors}")
    else:
        print("Inserted 200 records into sales_by_date.")


def insert_sample_events_by_hour():
    print("Inserting 200 random records into events_by_hour...")
    table_id = f"{DATASET_REF}.events_by_hour"
    rows = []
    base_time = datetime(2025, 5, 1, 0, 0, 0)
    event_types = ["click", "view", "purchase", "login"]
    devices = ["mobile", "desktop", "tablet"]
    for i in range(200):
        event_id = f"EV{i+1:04d}"
        event_timestamp = (
            base_time
            + timedelta(
                hours=randint(0, 48), minutes=randint(0, 59), seconds=randint(0, 59)
            )
        ).isoformat()
        event_type = choice(event_types)
        user_id = f"U{randint(1, 100):04d}"
        device = choice(devices)
        rows.append(
            {
                "event_id": event_id,
                "event_timestamp": event_timestamp,
                "event_type": event_type,
                "user_id": user_id,
                "device": device,
            }
        )
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"Errors inserting events_by_hour: {errors}")
    else:
        print("Inserted 200 records into events_by_hour.")


def insert_sample_logs_by_ingestion():
    print("Inserting 200 random records into logs_by_ingestion...")
    table_id = f"{DATASET_REF}.logs_by_ingestion"
    rows = []
    severities = ["INFO", "WARNING", "ERROR", "DEBUG"]
    sources = ["api", "web", "worker", "cron"]
    for i in range(200):
        log_id = f"L{i+1:04d}"
        if fake:
            log_message = fake.sentence()
        else:
            log_message = f"Log message {i+1}"
        severity = choice(severities)
        source = choice(sources)
        rows.append(
            {
                "log_id": log_id,
                "log_message": log_message,
                "severity": severity,
                "source": source,
            }
        )
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"Errors inserting logs_by_ingestion: {errors}")
    else:
        print("Inserted 200 records into logs_by_ingestion.")


def insert_sample_customers_by_age():
    print("Inserting 200 random records into customers_by_age...")
    table_id = f"{DATASET_REF}.customers_by_age"
    rows = []
    cities = ["Hanoi", "Saigon", "Danang", "Hue", "Cantho"]
    base_date = datetime(2020, 1, 1)
    for i in range(200):
        customer_id = f"C{randint(1, 1000):04d}"
        if fake:
            name = fake.name()
        else:
            name = f"Customer {i+1}"
        age = randint(10, 90)
        city = choice(cities)
        signup_date = (
            (base_date + timedelta(days=randint(0, 365 * 5))).date().isoformat()
        )
        rows.append(
            {
                "customer_id": customer_id,
                "name": name,
                "age": age,
                "city": city,
                "signup_date": signup_date,
            }
        )
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"Errors inserting customers_by_age: {errors}")
    else:
        print("Inserted 200 records into customers_by_age.")


def main():
    """Main function to create all partitioned tables and insert sample data."""
    print("Creating BigQuery partitioned tables...")
    # Create the dataset first
    create_dataset_if_not_exists()
    # Create different types of partitioned tables
    create_date_partitioned_table()
    create_timestamp_partitioned_table()
    create_ingestion_time_partitioned_table()
    create_integer_range_partitioned_table()
    print("All partitioned tables created successfully!")
    # Insert sample data
    insert_sample_sales_by_date()
    insert_sample_events_by_hour()
    insert_sample_logs_by_ingestion()
    insert_sample_customers_by_age()


if __name__ == "__main__":
    main()
