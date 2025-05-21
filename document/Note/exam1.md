# Databricks Certified Data Engineer Professional Practice Exam

## Instructions
- This practice exam contains 57 multiple-choice questions based on the topics from the Databricks Certified Data Engineer Professional certification.
- Select the best answer for each question.
- Answers are provided at the end of the document.

## Questions

### 1. How can you read parameters using `dbutils.widgets.text` and retrieve their values?
A. Use `dbutils.widgets.getValue()`
B. Use `dbutils.widgets.get()`
C. Use `dbutils.widgets.retrieve()`
D. Use `dbutils.widgets.read()`

### 2. How do you provide read access for a production notebook to a new data engineer for review?
A. Set the notebook's permissions to "Can Run"
B. Set the notebook's permissions to "Can Edit"
C. Set the notebook's permissions to "Can Read"
D. Set the notebook's permissions to "Can Manage"

### 3. When attaching a notebook to a cluster, which permission allows you to run the notebook?
A. "Can Attach"
B. "Can Execute"
C. "Can Restart"
D. "Can Run"

### 4. Should production DLT pipelines be run on a job cluster or an all-purpose cluster?
A. All-purpose cluster
B. Job cluster
C. Either can be used with the same results
D. Neither, DLT pipelines use their own dedicated clusters

### 5. Does a CTAS (CREATE TABLE AS SELECT) operation execute the load every time or only during table creation?
A. Only during table creation
B. Every time the table is accessed
C. It depends on the table properties
D. It depends on the query optimization settings

### 6. How can you control access to read production secrets using scope access control?
A. Set "Execute" permissions on the scope
B. Set "Read" permissions on the scope or secret
C. Set "Admin" permissions on the scope
D. Set "Write" permissions on the scope

### 7. Where does the `%sh` command run in Databricks?
A. On all worker nodes
B. On the driver node
C. On both driver and worker nodes
D. On a separate command node

### 8. If a query contains a filter, how does Databricks use file statistics in the transaction log?
A. It uses file-level min/max statistics to skip files that don't contain relevant data
B. It doesn't use file statistics for filtered queries
C. It only uses file statistics for partitioned tables
D. It only uses file statistics for optimized tables

### 9. What happens when you run a `VACUUM` command on a shallow clone table?
A. It successfully removes files older than the retention period
B. It results in an error
C. It vacuums the source table instead
D. It automatically converts the shallow clone to a deep clone first

### 10. Which type of join is not possible when performing a join between a static DataFrame and a streaming DataFrame?
A. Left join
B. Inner join
C. Right join
D. Full outer join

### 11. When the source is a CDC (Change Data Capture), what's the best approach for maintaining data consistency?
A. Use `INSERT OVERWRITE` for each batch
B. Use `MERGE INTO` operations
C. Leverage the Change Data Feed (CDF) feature
D. Use `COPY INTO` command

### 12. How can you find the difference between the previous and present commit in a Delta table?
A. Use `DESCRIBE HISTORY` and compare the versions
B. Use Change Data Feed (CDF) to track changes
C. Query the table with time travel syntax for both versions
D. Use the `DIFF` command between versions

### 13. What is the best approach for nightly jobs that overwrite a table for the business team with the least latency?
A. Write directly to the table nightly
B. Create a view on top of the underlying data
C. Use a materialized view that refreshes nightly
D. Create a shallow clone that updates nightly

### 14. What does the `OPTIMIZE TABLE` command do, and what is the target file size?
A. Compacts small files and the target file size is 256MB
B. Compacts small files and the target file size is 512MB
C. Compacts small files and the target file size is 1GB
D. Compacts small files and the target file size is 2GB

### 15. In a streaming scenario, what does the `.withWatermark` function do with a delay of 10 minutes?
A. Limits the amount of state maintained by dropping data older than 10 minutes
B. Delays processing of all data by 10 minutes
C. Sets a timeout for stream processing to 10 minutes
D. Batches data into 10-minute windows

### 16. How does aggregating on the source and then overwriting/appending to the target impact data load?
A. It reduces the amount of data transferred over the network
B. It increases processing time due to double aggregation
C. It has no impact on performance
D. It may lead to data inconsistency if not handled properly

### 17. Why might you receive three email notifications when a job was set to trigger an email if `mean(temp) > 120`?
A. The alert was configured incorrectly
B. There were three distinct temperature readings above 120
C. The job ran three times
D. Multiple batches within the same job run triggered the alert

### 18. Why should the checkpoint directory be unique for each stream in a streaming job?
A. To prevent data corruption
B. To improve performance
C. To make debugging easier
D. It's not required, streams can share checkpoint directories

### 19. How would you set up an Autoloader scenario to load data into a bronze table with history and update the target table?
A. Use `readStream` with `trigger(once=True)` and write mode "append"
B. Use `readStream` with continuous processing and write mode "complete"
C. Use `readStream` with `foreachBatch` to handle custom logic
D. Use batch processing with `spark.read()` and write mode "overwrite"

### 20. How can you handle streaming deduplication based on a unique identifier?
A. Use `dropDuplicates()` after reading the stream
B. Configure Autoloader with `deduplication` option
C. Use `.withWatermark()` and then `dropDuplicates()`
D. Create a Delta table with constraints

### 21. For batch loading, what happens if the load is set to overwrite mode?
A. It appends new data to the target table
B. It replaces the entire target table with the new data
C. It merges the new data with existing data
D. It fails if the target table already exists

### 22. In a Change Data Feed (CDF) scenario, if `readChangeFeed` starts at version 0 and append is used, will there be deduplication?
A. Yes, CDF automatically handles deduplication
B. No, there will be duplicate records
C. Only if explicitly configured with `deduplicate=true`
D. Only for tables with a defined primary key

### 23. How can you identify whether a table is SCD Type 1 or 2 based on an upsert operation?
A. SCD Type 1 overwrites records, SCD Type 2 maintains history
B. SCD Type 1 appends all records, SCD Type 2 merges records
C. SCD Type 1 uses a timestamp, SCD Type 2 doesn't
D. SCD Type 1 is streaming, SCD Type 2 is batch processing

### 24. To avoid performance issues in streaming jobs, should you decrease the trigger time?
A. Yes, shorter trigger intervals always improve performance
B. No, shorter trigger intervals can lead to more frequent small batches
C. It depends on the data volume and processing complexity
D. Trigger time has no impact on performance

### 25. How does Delta Lake decide on file skipping based on columns in a query?
A. It only skips files if all query columns have statistics
B. It can skip files if any column in the query has statistics
C. It skips files based on the table partitioning strategy
D. File skipping is only available for Z-ordered columns

### 26. What does granting "Usage" and "Select" permissions on a Delta table allow a user to do?
A. Read the table data only
B. Read and modify the table data
C. Read the table and use its schema in new tables
D. Full access to the table including schema modifications

### 27. How do you create an unmanaged table in Databricks?
A. Use `CREATE EXTERNAL TABLE`
B. Use `CREATE TABLE` with `LOCATION` specified
C. Use `CREATE TABLE` without `LOCATION`
D. Use `CREATE UNMANAGED TABLE`

### 28. What makes a date column a good candidate for partitioning in a Delta table?
A. High cardinality (many unique values)
B. Low cardinality (few unique values) with even distribution
C. It contains only numeric values
D. It contains only string values

### 29. What happens in the transaction log when you rename a Delta table using `ALTER TABLE xx RENAME xx`?
A. A new transaction log is created and the old one is deleted
B. The table name is updated in the existing transaction log
C. A metadata operation is recorded in the transaction log
D. The transaction log is not affected by rename operations

### 30. How would you handle an error with a check constraint violation?
A. Disable the constraint temporarily
B. Use `INSERT OVERWRITE` to replace all data
C. Fix the violation in the source data before loading
D. Use exception handling to skip invalid records

### 31. When using `DESCRIBE` commands, how can you retrieve table properties, comments, and partition details?
A. Use `DESCRIBE TABLE`
B. Use `DESCRIBE EXTENDED`
C. Use `DESCRIBE HISTORY`
D. Use `DESCRIBE DETAIL`

### 32. How are file statistics used in Delta Lake, and why are they important?
A. They provide record counts only
B. They track file modifications for auditing
C. They store min/max values for columns to enable data skipping
D. They enable parallel processing of files

### 33. In the Ganglia UI, how can you detect a spill during query execution?
A. Look for red warning indicators
B. Check the "Spills" tab
C. Look for disk I/O spikes and shuffle spill metrics
D. Monitor CPU utilization

### 34. If a repo branch is missing locally, how can you retrieve that branch with the latest code changes?
A. Use `git pull origin <branch_name>`
B. Use the Databricks UI to clone the repository again
C. Use `git fetch` followed by `git checkout <branch_name>`
D. Create a new branch with the same name

### 35. After deleting records with a query like `DELETE FROM A WHERE id IN (SELECT id FROM B)`, can you time travel to see the deleted records?
A. No, deleted records are permanently removed
B. Yes, using time travel with version numbers or timestamps
C. Only if the table has Change Data Feed enabled
D. Only if the deletion was part of a transaction

### 36. What are the differences between DBFS and mounts in Databricks?
A. DBFS is temporary, mounts are permanent
B. DBFS is a filesystem interface, mounts provide access to external storage
C. DBFS is for structured data, mounts are for unstructured data
D. DBFS is slower, mounts offer better performance

### 37. If the API `2.0/jobs/create` is executed three times with the same JSON, what will happen?
A. It will create one job
B. It will create three identical jobs
C. It will update the same job three times
D. It will return an error after the first execution

### 38. What is DBFS in Databricks?
A. Databricks File Storage, a proprietary file format
B. Databricks File System, an interface to access various storage systems
C. Databricks File Serializer, for optimizing file storage
D. Databricks File Service, for file transfer between clusters

### 39. How do you install a Python library using `%pip` in a Databricks notebook?
A. `%pip install <library-name>`
B. `%pip --install <library-name>`
C. `%pip add <library-name>`
D. `%pip package install <library-name>`

### 40. If Task 1 has downstream Task 2 and Task 3 running in parallel, and Task 1 and Task 2 succeed while Task 3 fails, what will be the final job status?
A. Success
B. Failed
C. Partially Completed
D. Error

### 41. How do you handle streaming job retries in production with job clusters?
A. Configure unlimited retries with exponential backoff
B. Set a maximum number of retries with a fixed interval
C. Use unlimited retries with a maximum of one concurrent run
D. Set up a separate monitoring job to restart failed jobs

### 42. How can you clone an existing job and version it using the Databricks CLI?
A. Use `databricks jobs get` followed by `databricks jobs create`
B. Use `databricks jobs clone --version`
C. Use `databricks jobs export` followed by `databricks jobs import`
D. Use `databricks jobs copy --new-version`

### 43. When converting a large JSON file (1TB) to Parquet with a partition size of 512 MB, what is the correct order of steps?
A. Read, repartition (2048 partitions), perform transformations, convert to Parquet
B. Read, perform narrow transformations, repartition (2048 partitions), convert to Parquet
C. Repartition first, read with partitioned input, transform, convert to Parquet
D. Read with adaptive query execution, transform, convert to Parquet

### 44. What happens in the target table when duplicates are dropped during a batch read and append operation?
A. Only unique records from the current batch are appended
B. All duplicates are removed from both the batch and existing data
C. An error is thrown requiring explicit handling
D. The operation automatically switches to "merge" behavior

### 45. If a column was missed during profiling from Kafka, how can you ensure that the data is fully replayable in the future?
A. Recreate the Kafka topic with the correct schema
B. Write raw data to a bronze table before transformation
C. Add the missing column to all existing data
D. Use schema evolution to handle the missing column

### 46. How do you handle access control for users in Databricks?
A. Only through workspace permissions
B. Using a combination of IAM roles, workspace permissions, and table ACLs
C. Exclusively through cluster policies
D. Using notebook-level permissions only

### 47. What is the use of the `pyspark.sql.functions.broadcast` function in a Spark job?
A. To distribute messages to all executors
B. To distribute a small DataFrame to all worker nodes for join optimization
C. To convert a streaming DataFrame to a batch DataFrame
D. To enable cross-cluster communication

### 48. What happens when performing a MERGE INTO with a condition "when not matched, insert *"?
A. Records from the source that don't match records in the target are inserted
B. All records from the source are inserted regardless of matches
C. Records that don't match a condition are filtered out
D. An error is thrown for records without matches

### 49. Given a function for loading bronze data, how would you write a silver load function to transform and update downstream tables?
A. Use the same approach but add transformation logic
B. Use `writeStream` with `foreachBatch` for incremental processing
C. Use batch processing with `MERGE INTO` operations
D. Use DLT pipelines with `APPLY CHANGES` syntax

### 50. If the code includes `CASE WHEN is_member("group") THEN email ELSE 'redacted' END AS email`, what will be the output if the user is not a member of the group?
A. NULL
B. The user's actual email
C. "redacted"
D. An empty string

### 51. How can you use the Ganglia UI to view logs and troubleshoot a Databricks job?
A. Access the "Logs" tab in the Ganglia UI
B. Ganglia doesn't provide logs, only metrics
C. Use the "Events" section in the Ganglia UI
D. Access the "Driver Logs" through the Spark UI in Ganglia

### 52. When working with multi-task jobs, how do you list or get the tasks using the API?
A. Use `2.0/jobs/list` with `include_tasks=true`
B. Use `2.0/jobs/tasks/list`
C. Use `2.0/jobs/run/list` to get run details including tasks
D. Use `2.0/tasks/list` with the job ID

### 53. What is unit testing in Databricks, and how is it applied?
A. Testing individual notebook cells
B. Testing full notebooks with different parameters
C. Testing individual functions using frameworks like pytest
D. Testing APIs using integration tests

### 54. What happens when multiple `display()` commands are executed repeatedly in development, and what is the impact in production?
A. Only the last `display()` shows results, with no production impact
B. All `display()` commands show results, causing memory issues in production
C. In production, `display()` commands are ignored
D. In production, `display()` commands write to logs instead of showing results

### 55. Will the `option("readChangeFeed")` work on a source Delta table with no Change Data Feed enabled?
A. Yes, it will work but only return the latest changes
B. No, it will throw an error
C. Yes, it will automatically enable CDF on the table
D. It will work but only for tables created after DBR 8.0

### 56. How can you identify whether a tumbling or sliding window is being used based on the code?
A. Tumbling windows use `window()`, sliding windows use `slidingWindow()`
B. Tumbling windows have equal window and slide duration, sliding windows have slide duration less than window duration
C. Tumbling windows use `groupBy().agg()`, sliding windows use `groupByWindow()`
D. Tumbling windows are stateless, sliding windows maintain state

### 57. What performance tuning considerations are involved with `spark.sql.files.maxPartitionBytes` and `spark.sql.shuffle.partitions`?
A. `maxPartitionBytes` controls the size of input partitions, `shuffle.partitions` controls the number of shuffle partitions
B. Both parameters control the same thing but at different stages
C. `maxPartitionBytes` is for reading, `shuffle.partitions` is for writing
D. They are only relevant for streaming applications

## Answers

1. B. Use `dbutils.widgets.get()`
2. C. Set the notebook's permissions to "Can Read"
3. C. "Can Restart"
4. B. Job cluster
5. A. Only during table creation
6. B. Set "Read" permissions on the scope or secret
7. B. On the driver node
8. A. It uses file-level min/max statistics to skip files that don't contain relevant data
9. B. It results in an error
10. C. Right join
11. B. Use `MERGE INTO` operations
12. B. Use Change Data Feed (CDF) to track changes
13. B. Create a view on top of the underlying data
14. C. Compacts small files and the target file size is 1GB
15. A. Limits the amount of state maintained by dropping data older than 10 minutes
16. A. It reduces the amount of data transferred over the network
17. D. Multiple batches within the same job run triggered the alert
18. A. To prevent data corruption
19. A. Use `readStream` with `trigger(once=True)` and write mode "append"
20. C. Use `.withWatermark()` and then `dropDuplicates()`
21. B. It replaces the entire target table with the new data
22. B. No, there will be duplicate records
23. A. SCD Type 1 overwrites records, SCD Type 2 maintains history
24. B. No, shorter trigger intervals can lead to more frequent small batches
25. A. It only skips files if all query columns have statistics
26. A. Read the table data only
27. B. Use `CREATE TABLE` with `LOCATION` specified
28. B. Low cardinality (few unique values) with even distribution
29. C. A metadata operation is recorded in the transaction log
30. C. Fix the violation in the source data before loading
31. B. Use `DESCRIBE EXTENDED`
32. C. They store min/max values for columns to enable data skipping
33. C. Look for disk I/O spikes and shuffle spill metrics
34. C. Use `git fetch` followed by `git checkout <branch_name>`
35. B. Yes, using time travel with version numbers or timestamps
36. B. DBFS is a filesystem interface, mounts provide access to external storage
37. B. It will create three identical jobs
38. B. Databricks File System, an interface to access various storage systems
39. A. `%pip install <library-name>`
40. B. Failed
41. C. Use unlimited retries with a maximum of one concurrent run
42. A. Use `databricks jobs get` followed by `databricks jobs create`
43. B. Read, perform narrow transformations, repartition (2048 partitions), convert to Parquet
44. A. Only unique records from the current batch are appended
45. B. Write raw data to a bronze table before transformation
46. B. Using a combination of IAM roles, workspace permissions, and table ACLs
47. B. To distribute a small DataFrame to all worker nodes for join optimization
48. A. Records from the source that don't match records in the target are inserted
49. B. Use `writeStream` with `foreachBatch` for incremental processing
50. C. "redacted"
51. B. Ganglia doesn't provide logs, only metrics
52. C. Use `2.0/jobs/run/list` to get run details including tasks
53. C. Testing individual functions using frameworks like pytest
54. A. Only the last `display()` shows results, with no production impact
55. B. No, it will throw an error
56. B. Tumbling windows have equal window and slide duration, sliding windows have slide duration less than window duration
57. A. `maxPartitionBytes` controls the size of input partitions, `shuffle.partitions` controls the number of shuffle partitions
