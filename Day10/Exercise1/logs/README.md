# Logs Directory

This directory contains log files from the various components of the data pipeline. After running the pipeline, you should see the following log files:

## Expected Log Files

1. **Kafka Producer Logs**
   - Filename: `kafka_producer.log`
   - Content: Logs from the Kafka producer showing stock data being sent to Kafka
   
   Example:
   ```
   2023-08-10 12:34:56,789 - stock-market-producer - INFO - Producer initialized with bootstrap servers: localhost:9092
   2023-08-10 12:34:56,790 - stock-market-producer - INFO - Producing to topic: stock-market-data
   2023-08-10 12:34:56,891 - stock-market-producer - INFO - Starting Stock Market data streaming...
   2023-08-10 12:34:57,123 - stock-market-producer - INFO - Sent: AAPL - Price: 152.42 - Volume: 5463
   ```

2. **Kafka Consumer Logs**
   - Filename: `kafka_consumer.log`
   - Content: Logs from the Kafka consumer showing stock data being received and saved
   
   Example:
   ```
   2023-08-10 12:35:01,234 - stock-market-consumer - INFO - Consumer initialized with bootstrap servers: localhost:9092
   2023-08-10 12:35:01,235 - stock-market-consumer - INFO - Consuming from topic: stock-market-data
   2023-08-10 12:35:01,236 - stock-market-consumer - INFO - Consumer group: stock-market-group
   2023-08-10 12:35:01,453 - stock-market-consumer - INFO - Received: AAPL - Price: 152.42 - Volume: 5463
   ```

3. **Spark Job Logs**
   - Filename: `spark_job.log`
   - Content: Logs from the Spark processing job showing data analysis and warehouse loading
   
   Example:
   ```
   2023-08-10 12:36:12,345 - stock-market-processor - INFO - Initializing Spark Stock Market Processor
   2023-08-10 12:36:15,678 - stock-market-processor - INFO - Spark session created with application ID: local-12345
   2023-08-10 12:36:17,890 - stock-market-processor - INFO - Processing stock market data from ../data
   2023-08-10 12:36:20,123 - stock-market-processor - INFO - Daily statistics saved to ../output/daily_stats
   ```

4. **Kestra Execution Logs**
   - These logs are available in the Kestra UI
   - They show the entire workflow execution from start to finish

## Log Rotation

For a production environment, these logs would typically be rotated to prevent disk space issues. For this exercise, the logs are kept simple for easy review.

## Troubleshooting

If you encounter issues with the pipeline, these logs are the first place to check for error messages and debugging information. 