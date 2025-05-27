# Lịch sử câu hỏi đã làm

1. An upstream system has been configured to pass the date for a given batch of data to the Databricks jobs API as a parameter. The notebook to be scheduled will use this parameter to load data with the following code: df = spark.read.format("parquet").load(f"/mnt/source/{date}")
Which code block should be used to create the date Python variable used in the above code block?

**Các lựa chọn:**
- a) date = spark.conf.get("date")
- b) input_dict = input(); date = input_dict["date"]
- c) import sys; date = sys.argv[1]
- d) date = dbutils.notebooks.getParam("date")
- e) dbutils.widgets.text("date", "null"); date = dbutils.widgets.get("date")

**Đáp án đúng:**
e) dbutils.widgets.text("date", "null"); date = dbutils.widgets.get("date")

2. The Databricks workspace administrator has configured interactive clusters for each of the data engineering groups. To control costs, clusters are set to terminate after 30 minutes of inactivity. Each user should be able to execute workloads against their assigned clusters at any time of the day. Assuming users have been added to a workspace but not granted any permissions, which of the following describes the minimal permissions a user would need to start and attach to an already configured cluster?

**Các lựa chọn:**
- a) Cluster creation allowed, "Can Restart" privileges on the required cluster
- b) Workspace Admin privileges, cluster creation allowed, "Can Attach To" privileges on the required cluster
- c) "Can Restart" privileges on the required cluster
- d) "Can Manage" privileges on the required cluster
- e) Cluster creation allowed, "Can Attach To" privileges on the required cluster

**Đáp án đúng (gần đúng nhất):**
- c) "Can Restart" privileges on the required cluster

3. The data engineering team has configured a Databricks SQL query and alert to monitor the values in a Delta Lake table. The recent_sensor_recordings table contains an identifying sensor_id alongside the timestamp and temperature for the most recent 5 minutes of recordings.

The query on the left is used to create the alert:

SELECT MEAN(temperature), MAX(temperature), MIN(temperature)
FROM recent_sensor_recordings
GROUP BY sensor_id

The query is set to refresh each minute and always completes in less than 10 seconds. The alert is set to trigger when mean(temperature) > 120. Notifications are triggered to be sent at most every 1 minute. If this alert raises notifications for 3 consecutive minutes and then stops, which statement must be true?

**Các lựa chọn:**
- The total average temperature across all sensors exceeded 120 on three consecutive executions of the query
- The recent_sensor_recordings table was unresponsive for three consecutive runs of the query
- The source query failed to update properly for three consecutive minutes and then restarted
- The maximum temperature recording for at least one sensor exceeded 120 on three consecutive executions of the query
- The average temperature recordings for at least one sensor exceeded 120 on three consecutive executions of the query

**Đáp án đúng:**
- The average temperature recordings for at least one sensor exceeded 120 on three consecutive executions of the query

4. A junior developer complains that the code in their notebook isn't producing the correct results in the development environment. A shared screenshot reveals that while they're using a notebook versioned with Databricks Repos, they're using a personal branch that contains old logic. The desired branch named dev-2.3.9 is not available from the branch selection dropdown.
Which approach will allow this developer to review the current logic for this notebook?

**Các lựa chọn:**
- Use Repos to make a pull request use the Databricks REST API to update the current branch to dev-2.3.9
- Use Repos to pull changes from the remote Git repository and select the dev-2.3.9 branch.  
- Use Repos to checkout the dev-2.3.9 branch and auto-resolve conflicts with the current branch
- Merge all changes back to the main branch in the remote Git repository and clone the repo again
- Use Repos to merge the current branch and the dev-2.3.9 branch, then make a pull request to sync with the remote repository

**Đáp án đúng:**
- Use Repos to pull changes from the remote Git repository and select the dev-2.3.9 branch.

5. The data science team has created and logged a production model using MLflow. The following code correctly imports and applies the production model to output the predictions as a new DataFrame named preds with the schema "customer_id LONG, predictions DOUBLE, date DATE". The data science team would like predictions saved to a Delta Lake table with the ability to compare all predictions across time. Churn predictions will be made at most once per day. Which code block accomplishes this task while minimizing potential compute costs?

**Các lựa chọn:**
a) preds.write.mode("append").saveAsTable("churn_preds")
b) preds.write.format("delta").save("/preds/churn_preds")
c) (preds.writeStream
    .outputMode("overwrite")
    .option("checkpointPath", "/_checkpoints/churn_preds")
    .start("/preds/churn_preds")
   )
d) (preds.writeStream
    .outputMode("append")
    .option("checkpointPath", "/_checkpoints/churn_preds")
    .table("churn_preds")
   )
e) (preds.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("churn_preds")
   )

**Đáp án đúng:**
a) preds.write.mode("append").saveAsTable("churn_preds")

6. An upstream source writes Parquet data as hourly batches to directories named with the current date. A nightly batch job runs the following code to ingest all data from the previous day as indicated by the date variable:

(spark.read
  .format("parquet")
  .load(f"/mnt/raw/orders/{date}")
  .dropDuplicates(["customer_id", "order_id"])
  .write
  .mode("append")
  .saveAsTable("orders")
)

Assume that the fields customer_id and order_id serve as a composite key to uniquely identify each order. If the upstream system is known to occasionally produce duplicate entries for a single order hours apart, which statement is correct?

**Các lựa chọn:**
a) Each write to the orders table will only contain unique records, and only those records without duplicates in the target table will be written.
b) Each write to the orders table will only contain unique records, but newly written records may have duplicates already present in the target table.
c) Each write to the orders table will run deduplication over the union of new and existing records, ensuring no duplicate records are present.
d) Each write to the orders table will only contain unique records; if existing records with the same key are present in the target table, the operation will fail.
e) Each write to the orders table will only contain unique records; if existing records with the same key are present in the target table, these records will be overwritten.

**Đáp án đúng:**
b) Each write to the orders table will only contain unique records, but newly written records may have duplicates already present in the target table.
