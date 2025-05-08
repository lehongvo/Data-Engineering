# Exercise 5: Error Handling and Dead Letter Queues in Kafka

This exercise focuses on error handling in Kafka systems, particularly using Dead Letter Queues (DLQ) to effectively manage error records.

## Exercise Description

In real-world data processing systems, errors are inevitable. Handling errors effectively is crucial to ensure stable and reliable system operation. This exercise simulates a data processing flow with an error handling mechanism through DLQ.

## Key Concepts

1. **Error Detection in Data**:
   - Producer sends both valid and invalid data
   - Consumer detects error records such as incorrect format or missing critical data

2. **Dead Letter Queue (DLQ)**:
   - Error records that cannot be processed are routed to a separate topic called DLQ
   - DLQ allows monitoring and analyzing issues without disrupting the main pipeline

3. **Error Monitoring and Logging**:
   - DLQ Consumer reads errors and logs details
   - Supports efficient investigation, error handling, and improves system reliability

## System Components

1. **Producer**: Creates and sends data (including both valid and invalid data)
2. **Main Consumer**: Processes data and detects errors, routes error records to DLQ
3. **DLQ Consumer**: Reads and logs error records from DLQ
4. **Error Analyzer**: Tracks and categorizes common error types

## How to Run the Exercise

1. Start the Kafka environment:
   ```
   ./run.sh
   ```

2. Observe the logs:
   - Producer logs: `producer.log`
   - Consumer logs: `consumer.log`
   - DLQ Consumer logs: `dlq_consumer.log`
   - Error Analytics logs: `error_analytics.log`

## What to Learn from this Exercise

- How to build robust error handling systems in Kafka
- Implementing the Dead Letter Queue pattern
- Techniques for detecting, categorizing, and handling different types of data errors
- Designing data recovery strategies and retry mechanisms 