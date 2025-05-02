# BigQuery Partitioning Exercise

This exercise demonstrates how to use BigQuery's partitioning features to optimize query performance when working with large datasets.

## What is BigQuery Partitioning?

Partitioning in BigQuery divides your tables into segments based on specific columns or time periods. This can significantly improve query performance and reduce costs by limiting the amount of data scanned.

## Types of Partitioning in BigQuery

1. **Time-unit column partitioning**: Partition by HOUR, DAY, MONTH, or YEAR based on a TIMESTAMP, DATE, or DATETIME column
2. **Ingestion-time partitioning**: Partition by the data's load time
3. **Integer range partitioning**: Partition based on an integer column's ranges
4. **Clustering**: While not technically partitioning, clustering organizes data based on contents of specific columns

## Benefits

- Reduced query costs (pay only for data scanned)
- Improved query performance
- Simplified data lifecycle management

## Files in this Exercise

- `create_partitioned_table.py`: Script to create partitioned tables in BigQuery
- `sample_queries.sql`: Example queries optimized with partition filters
- `partition_metadata.py`: Script to examine partition metadata
- `data/`: Sample data to load into partitioned tables

## Instructions

1. Review the scripts and queries in this directory
2. Run `create_partitioned_table.py` to set up sample partitioned tables
3. Execute the queries in `sample_queries.sql` to see partition pruning in action
4. Analyze query performance with and without partition filters