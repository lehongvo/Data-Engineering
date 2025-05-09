# Kafka Streams Application - Text to Uppercase

This is a simple Kafka Streams application that reads text from an input topic, converts it to uppercase, and writes it to an output topic.

## Prerequisites

- Docker and Docker Compose
- Python 3.6+
- pip (Python package manager)

## Setup and Run

1. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start Kafka and create topics**

   Make the run script executable and run it:

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   This will start Kafka and Zookeeper in Docker containers and create the required topics.

3. **Run the Kafka Streams application**

   ```bash
   python kafka_uppercase.py
   ```

4. **Test the application**

   Open two terminal windows:

   a. In the first terminal, start a producer to send messages to the input topic:

   ```bash
   docker exec -it e1-kafka-1 kafka-console-producer --broker-list localhost:9094 --topic input-topic
   ```

   b. In the second terminal, start a consumer to read messages from the output topic:

   ```bash
   docker exec -it e1-kafka-1 kafka-console-consumer --bootstrap-server localhost:9094 --topic output-topic --from-beginning
   ```

   c. Type some text in the producer terminal and press Enter. You should see the uppercase version of your text in the consumer terminal.

5. **Shutdown**

   When you're done, press Ctrl+C to stop the Kafka Streams application, then run:

   ```bash
   docker-compose down
   ```

   to shut down the Kafka and Zookeeper containers.

## Logging

All input and output messages are logged in the `log` directory:
- `log/input.log`: Contains all messages received from the input topic
- `log/output.log`: Contains all transformed messages and processing information

When running the producer and consumer with the suggested commands, the messages will also be logged to these files.

## Troubleshooting

If you encounter connection issues:

1. **Check Kafka Status**: Verify that Kafka and Zookeeper containers are running:
   ```bash
   docker ps
   ```

2. **Connection Issues**: If you see connection errors, try restarting the environment:
   ```bash
   ./run.sh
   # Choose option 1 to restart the environment
   ```

3. **View Logs**: Check the logs for more details:
   ```bash
   cat log/output.log
   ```

4. **Container Networking**: Make sure that the container networking is working correctly.
   Kafka inside the container is accessible via `kafka:9092` and from outside via `localhost:9094`.
