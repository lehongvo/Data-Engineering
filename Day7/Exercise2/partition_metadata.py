#!/usr/bin/env python3

from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

"""
This script demonstrates how to analyze partition metadata in BigQuery.
It shows how to retrieve information about partitions and visualize partition statistics.
"""

# Set up the BigQuery client
client = bigquery.Client()

# Set your project and dataset information
PROJECT_ID = "unique-axle-457602-n6"  # Replace with your Google Cloud project ID
DATASET_ID = "partitioning_demo"
DATASET_REF = f"{PROJECT_ID}.{DATASET_ID}"


def get_table_partitions(table_id):
    """
    Get information about all partitions in a table.
    """
    query = f"""
    SELECT
        table_name,
        partition_id,
        total_rows,
        total_logical_bytes / POWER(1024, 3) as size_gb,
        last_modified_time
    FROM
        `{DATASET_REF}.INFORMATION_SCHEMA.PARTITIONS`
    WHERE
        table_name = '{table_id}'
    ORDER BY
        partition_id
    """

    return client.query(query).to_dataframe()


def vanalyze_date_partitioned_table():
    """
    Analyze the partitions of the date-partitioned sales table.
    """
    print("Analyzing partitions for sales_by_date table...")
    df = get_table_partitions("sales_by_date")

    print(f"Total partitions: {len(df)}")
    print("\nPartition statistics:")
    print(df.describe())

    print("\nSample partition data:")
    print(df.head())

    # Create a bar chart of partition sizes
    plt.figure(figsize=(12, 6))
    plt.bar(df["partition_id"], df["size_gb"])
    plt.xlabel("Partition ID")
    plt.ylabel("Size (GB)")
    plt.title("Size of Each Partition in sales_by_date Table")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("data/sales_partition_sizes.png")
    plt.close()

    return df


def analyze_query_performance():
    """
    Run performance tests comparing queries with and without partition filters.
    """
    print("\nAnalyzing query performance with and without partition filters...")

    # Query with partition filter
    query_with_filter = f"""
    SELECT
      transaction_date,
      COUNT(*) as tx_count,
      SUM(amount) as total_amount
    FROM
      `{DATASET_REF}.sales_by_date`
    WHERE
      transaction_date BETWEEN '2025-01-01' AND '2025-01-31'
    GROUP BY
      transaction_date
    """

    # Query without partition filter
    query_without_filter = f"""
    SELECT
      transaction_date,
      COUNT(*) as tx_count,
      SUM(amount) as total_amount
    FROM
      `{DATASET_REF}.sales_by_date`
    GROUP BY
      transaction_date
    HAVING
      transaction_date BETWEEN '2025-01-01' AND '2025-01-31'
    """

    # Run queries and measure performance
    start_time = datetime.now()
    job = client.query(query_with_filter)
    result1 = job.result()
    duration1 = (datetime.now() - start_time).total_seconds()
    bytes_processed1 = job.total_bytes_processed

    start_time = datetime.now()
    job = client.query(query_without_filter)
    result2 = job.result()
    duration2 = (datetime.now() - start_time).total_seconds()
    bytes_processed2 = job.total_bytes_processed

    # Display results
    print("\nPerformance Comparison:")
    print(f"Query with partition filter:")
    print(f"  - Duration: {duration1:.2f} seconds")
    print(f"  - Bytes processed: {bytes_processed1 / (1024**3):.2f} GB")

    print(f"\nQuery without partition filter:")
    print(f"  - Duration: {duration2:.2f} seconds")
    print(f"  - Bytes processed: {bytes_processed2 / (1024**3):.2f} GB")

    print(f"\nImprovement with partition filter:")
    print(f"  - Time reduction: {(duration2 - duration1) / duration2 * 100:.2f}%")
    print(
        f"  - Bytes reduction: {(bytes_processed2 - bytes_processed1) / bytes_processed2 * 100:.2f}%"
    )

    # Create comparison chart
    categories = ["With Partition Filter", "Without Partition Filter"]
    times = [duration1, duration2]
    data_processed = [bytes_processed1 / (1024**3), bytes_processed2 / (1024**3)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.bar(categories, times, color=["green", "red"])
    ax1.set_ylabel("Query Duration (seconds)")
    ax1.set_title("Query Performance Comparison")

    ax2.bar(categories, data_processed, color=["green", "red"])
    ax2.set_ylabel("Data Processed (GB)")
    ax2.set_title("Data Scanned Comparison")

    plt.tight_layout()
    plt.savefig("data/query_performance_comparison.png")
    plt.close()


def analyze_time_partitioning_impact():
    """
    Generate a report on how time partitioning affects table storage and access patterns.
    """
    print("\nGenerating time partitioning impact report...")

    # Create a sample query to analyze event distribution by hour
    query = f"""
    SELECT
      FORMAT_TIMESTAMP('%Y-%m-%d-%H', event_timestamp) as hourly_partition,
      COUNT(*) as event_count,
      COUNT(DISTINCT user_id) as unique_users
    FROM
      `{DATASET_REF}.events_by_hour`
    GROUP BY
      hourly_partition
    ORDER BY
      hourly_partition
    """

    # Note: This query would execute if the table had data
    # For demo purposes, we'll simulate the results
    print("(Simulating results for demonstration purposes)")

    # Create simulated hourly data
    start_date = datetime(2025, 5, 1)
    hours = 48  # 2 days worth of hours

    hourly_partition = [
        (start_date + timedelta(hours=i)).strftime("%Y-%m-%d-%H") for i in range(hours)
    ]
    event_count = [
        1000 + i * 50 + (i % 24) * 200 for i in range(hours)
    ]  # Daily pattern
    unique_users = [
        int(count * 0.7) for count in event_count
    ]  # 70% of events from unique users

    # Create a DataFrame from simulated data
    df = pd.DataFrame(
        {
            "hourly_partition": hourly_partition,
            "event_count": event_count,
            "unique_users": unique_users,
        }
    )

    print("\nHourly event statistics (sample):")
    print(df.head())

    # Create visualization of hourly patterns
    plt.figure(figsize=(14, 6))
    plt.plot(df["hourly_partition"], df["event_count"], "b-", label="Total Events")
    plt.plot(df["hourly_partition"], df["unique_users"], "r--", label="Unique Users")
    plt.xlabel("Hour")
    plt.ylabel("Count")
    plt.title("Event Distribution by Hour")
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig("data/hourly_event_distribution.png")
    plt.close()

    # Output recommendations
    print("\nPartitioning Recommendations:")
    print(
        "1. Based on the hourly patterns, HOUR partitioning is optimal for this event data"
    )
    print("2. For less frequent events, consider using DAY partitioning instead")
    print(
        "3. For tables that will exceed 1000 partitions in a year, consider using MONTH"
    )
    print(
        "4. Add clustering on frequently filtered columns like 'event_type' and 'user_id'"
    )


def main():
    """Main function to analyze partition metadata."""
    print("BigQuery Partition Analysis Tool")
    print("=" * 40)

    # Create data directory if it doesn't exist
    import os

    os.makedirs("data", exist_ok=True)

    # Note: These functions assume the tables exist and have data
    # For real use, remove the comments and execute these functions
    print("Note: This is a demonstration script. In a real environment with")
    print("actual data, these functions would provide valuable partition insights.")
    print("To use with real data, make sure to update the PROJECT_ID variable.")

    # When you have actual data, uncomment these lines:
    # analyze_date_partitioned_table()
    # analyze_query_performance()
    # analyze_time_partitioning_impact()

    print(
        "\nIn a real environment, this script would generate visualizations in the data/ directory."
    )
    print(
        "The visualizations would show partition sizes, query performance comparisons,"
    )
    print(
        "and event distribution patterns to help optimize your partitioning strategy."
    )


if __name__ == "__main__":
    main()
