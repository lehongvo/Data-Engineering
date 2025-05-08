# Exercise 6: Kafka Streams for Real-time Processing

This exercise demonstrates the use of Kafka Streams for real-time data processing, focusing on three key real-time analytics patterns:

## Key Features

1. **Anomaly Detection and Filtering**:
   - Detecting abnormal sensor values from temperature, humidity, and pressure sensors
   - Generating real-time alerts when anomalies are detected
   - Monitoring critical thresholds for quick response

2. **Time-Windowed Aggregations**:
   - Calculating average values over specific time windows
   - Analyzing trends in temperature, humidity, and pressure data
   - Providing a real-time dashboard of environmental conditions

3. **Stream Joining**:
   - Combining data from multiple sensor sources
   - Creating a comprehensive view of conditions across different locations
   - Enabling cross-sensor analytics

## System Architecture

The system consists of the following components:

1. **Sensor Data Producer** (`sensor_producer.py`):
   - Generates simulated sensor data (temperature, humidity, pressure)
   - Introduces occasional anomalies for testing
   - Publishes data to Kafka topics: `temperature-data`, `humidity-data`, `pressure-data`

2. **Stream Processor** (`stream_processor.py`):
   - Consumes data from all sensor topics
   - Performs real-time stream processing:
     - Detects and flags anomalies
     - Calculates time-windowed averages
     - Joins data from different sensor streams
   - Publishes processed data to output topics: `anomaly-alerts`, `window-aggregates`, `joined-sensor-data`

3. **Result Consumer** (`result_consumer.py`):
   - Displays processed data in a readable format
   - Shows anomaly alerts, time-windowed averages, and joined sensor data
   - Provides a monitoring dashboard for the system

## Data Flow

1. Sensors publish data to their respective topics
2. Stream processor consumes and processes the data
3. Processed results are published to output topics
4. Result consumer displays the processed data

## How to Run

1. Ensure Docker is running on your system
2. Run the following command to start the exercise:
   ```
   ./run.sh
   ```

3. The system will:
   - Set up Kafka and required topics
   - Start the stream processor
   - Start the result consumer
   - Start the sensor data producer

4. Observe the output in the terminal or check individual logs:
   - `sensor_producer.log`
   - `stream_processor.log`
   - `result_consumer.log`

5. To stop the system, press `Ctrl+C` in the terminal running the script

## Learning Outcomes

- Understanding Kafka Streams for real-time processing
- Implementing key stream processing patterns:
  - Filtering and alerting
  - Windowed aggregations
  - Stream joining
- Designing robust real-time data pipelines
- Working with time-based operations in streaming data 