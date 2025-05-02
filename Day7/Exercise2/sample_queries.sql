-- BigQuery Partitioned Table Queries
-- This file contains examples of optimized queries using partition filters

-- -------------------------------------------------------------------------
-- 1. DATE PARTITIONED TABLE QUERIES
-- -------------------------------------------------------------------------

-- Query with a partition filter (efficient - scans only one partition)
-- This query will only scan the data from February 1, 2025
SELECT 
  transaction_id, 
  product_id, 
  amount
FROM `unique-axle-457602-n6.partitioning_demo.sales_by_date`
WHERE transaction_date = '2025-02-01'
ORDER BY amount DESC
LIMIT 100;

-- Query with a partition range (efficient - scans only specified partitions)
-- This will only scan data from the last 30 days
SELECT 
  transaction_date,
  SUM(amount) as daily_sales
FROM `unique-axle-457602-n6.partitioning_demo.sales_by_date`
WHERE transaction_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND CURRENT_DATE()
GROUP BY transaction_date
ORDER BY transaction_date;

-- Query without partition filter (inefficient - scans all partitions)
-- Avoid this pattern as it scans the entire table
SELECT 
  COUNT(*) as total_transactions,
  SUM(amount) as total_sales
FROM `unique-axle-457602-n6.partitioning_demo.sales_by_date`
-- Missing WHERE clause with transaction_date

-- -------------------------------------------------------------------------
-- 2. TIMESTAMP PARTITIONED TABLE QUERIES
-- -------------------------------------------------------------------------

-- Query with hourly partition filter (efficient)
-- This will only scan data from a specific hour
SELECT 
  event_id,
  event_type,
  user_id
FROM `unique-axle-457602-n6.partitioning_demo.events_by_hour`
WHERE 
  event_timestamp >= TIMESTAMP('2025-05-01 08:00:00')
  AND event_timestamp < TIMESTAMP('2025-05-01 09:00:00')
ORDER BY event_timestamp;

-- Query with compound partition and clustering filter (very efficient)
-- Uses both partitioning and clustering for maximum performance
SELECT 
  event_id,
  event_timestamp,
  device
FROM `unique-axle-457602-n6.partitioning_demo.events_by_hour`
WHERE 
  event_timestamp >= TIMESTAMP('2025-05-01') 
  AND event_timestamp < TIMESTAMP('2025-05-02')
  AND event_type = 'login'
  AND user_id = 'user123'
ORDER BY event_timestamp;

-- -------------------------------------------------------------------------
-- 3. INGESTION TIME PARTITIONING QUERIES
-- -------------------------------------------------------------------------

-- Query with _PARTITIONTIME pseudo column (efficient)
-- This will scan only the specific day's partition
SELECT 
  log_id,
  log_message,
  severity
FROM `unique-axle-457602-n6.partitioning_demo.logs_by_ingestion`
WHERE _PARTITIONTIME = TIMESTAMP('2025-05-01')
ORDER BY severity DESC;

-- Query with _PARTITIONDATE (alternative syntax)
SELECT 
  COUNT(*) as error_count
FROM `unique-axle-457602-n6.partitioning_demo.logs_by_ingestion`
WHERE 
  _PARTITIONDATE BETWEEN DATE('2025-04-15') AND DATE('2025-04-30')
  AND severity = 'ERROR';

-- -------------------------------------------------------------------------
-- 4. INTEGER RANGE PARTITIONING QUERIES
-- -------------------------------------------------------------------------

-- Query with integer partition filter (efficient)
-- This will scan only the partition containing ages 20-29
SELECT 
  customer_id,
  name,
  city
FROM `unique-axle-457602-n6.partitioning_demo.customers_by_age`
WHERE age >= 20 AND age < 30
ORDER BY age;

-- Query with partition pruning and additional filters
SELECT 
  COUNT(*) as customer_count,
  city
FROM `unique-axle-457602-n6.partitioning_demo.customers_by_age`
WHERE 
  age >= 30 AND age < 50  -- Limits to 2 partitions (30-39, 40-49)
  AND city = 'New York'
GROUP BY city;

-- -------------------------------------------------------------------------
-- 5. PARTITION METADATA QUERIES
-- -------------------------------------------------------------------------

-- View partitioning information
SELECT
  table_name,
  partition_id,
  total_rows,
  total_logical_bytes,
  last_modified_time
FROM
  `unique-axle-457602-n6.partitioning_demo.INFORMATION_SCHEMA.PARTITIONS`
WHERE
  table_name = 'sales_by_date'
ORDER BY
  partition_id DESC;

-- Check the size and number of rows by partition
SELECT
  FORMAT_TIMESTAMP('%Y%m%d', _PARTITIONTIME) as partition_date,
  COUNT(*) as row_count,
  SUM(IF(severity = 'ERROR', 1, 0)) as error_count,
  SUM(IF(severity = 'WARNING', 1, 0)) as warning_count
FROM
  `unique-axle-457602-n6.partitioning_demo.logs_by_ingestion`
GROUP BY
  partition_date
ORDER BY
  partition_date DESC;

-- -------------------------------------------------------------------------
-- 6. PERFORMANCE COMPARISON
-- -------------------------------------------------------------------------

-- Query with partition filter (record execution time and bytes scanned)
SELECT
  transaction_date,
  COUNT(*) as tx_count,
  SUM(amount) as total_amount
FROM
  `unique-axle-457602-n6.partitioning_demo.sales_by_date`
WHERE
  transaction_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY
  transaction_date;

-- Same query without partition filter (compare execution time and bytes scanned)
SELECT
  transaction_date,
  COUNT(*) as tx_count,
  SUM(amount) as total_amount
FROM
  `unique-axle-457602-n6.partitioning_demo.sales_by_date`
GROUP BY
  transaction_date
HAVING
  transaction_date BETWEEN '2025-01-01' AND '2025-01-31';