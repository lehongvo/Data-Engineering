# Kafka Streams Temperature Processing Exercise (E2)

This exercise demonstrates a real-time temperature data processing application using Kafka Streams to:
1. Calculate 5-minute average temperatures from multiple sensors
2. Detect abnormal temperature readings (above 30°C)

## Architecture

The application consists of:

- **Temperature Producer**: Simulates temperature sensors that send readings to Kafka
- **Temperature Processor**: Consumes temperature readings, calculates 5-minute averages, and detects abnormal readings
- **Three Kafka Topics**:
  - `temperature-readings`: Raw temperature data from sensors
  - `temperature-averages`: Calculated 5-minute average temperatures per sensor
  - `temperature-alerts`: Alerts for abnormal temperature readings (>30°C)

## Prerequisites

- Docker and Docker Compose
- Python 3.7+
- pip3

## Running the Application

We've provided a convenient script to setup and run the application:

```bash
./run.sh
```

This will display a menu with the following options:

1. **Setup environment**: Install dependencies, start Kafka, create topics
2. **Run Temperature Producer**: Start the simulated sensor data producer
3. **Run Temperature Processor**: Start the main processing application
4. **Run Temperature Averages Consumer**: View the 5-minute average temperature calculations
5. **Run Temperature Alerts Consumer**: View the abnormal temperature alerts
6. **Run Manual Temperature Producer**: Manually send temperature readings

## Normal Workflow

For the typical workflow, follow these steps:

1. Open 4 terminal windows/tabs
2. In the first terminal, run option 1 to setup the environment
3. In the first terminal, run option 3 to start the temperature processor
4. In the second terminal, run option 2 to start the temperature producer
5. In the third terminal, run option 4 to view the average temperatures
6. In the fourth terminal, run option 5 to view abnormal temperature alerts

## Data Format

Temperature readings are formatted as JSON:

```json
{
  "sensorId": "sensor-001",
  "temperature": 25.5,
  "timestamp": "2023-01-01T12:00:00.000Z",
  "unit": "Celsius"
}
```

Average temperature output:

```json
{
  "timestamp": "2023-01-01T12:05:00.000Z",
  "window_size_minutes": 5,
  "averages": {
    "sensor-001": 24.5,
    "sensor-002": 22.7,
    "sensor-003": 31.2
  }
}
```

Alert output:

```json
{
  "timestamp": "2023-01-01T12:03:00.000Z",
  "sensorId": "sensor-003",
  "temperature": 32.5,
  "threshold": 30.0,
  "message": "Abnormal temperature detected: 32.5°C exceeds threshold of 30.0°C"
}
```

## Producer Configuration

The temperature producer can be configured with command line arguments:

```bash
python3 temperature_producer.py --interval 1.0 --abnormal-rate 0.15 --count 100
```

- `--interval`: Time between readings in seconds (default: 1.0)
- `--abnormal-rate`: Probability of generating abnormal readings (default: 0.1)
- `--count`: Number of readings to generate (0 for continuous, default: 0)

## Troubleshooting

If you encounter connection issues:

1. Ensure Docker containers are running: `docker ps`
2. Check logs in the `log/` directory
3. Verify that Kafka is accessible on port 9094: `telnet localhost 9094`
4. Restart the environment with option 1

## Implementation Details

- Temperature windowing is handled using a custom class that maintains a sliding window of readings
- Averages are calculated and published every 30 seconds
- Abnormal temperature detection occurs in real-time as messages are processed 