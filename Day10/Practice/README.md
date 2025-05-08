# Ethereum Blockchain Real-time Data Processing with Kafka and Spark

Real-time Ethereum blockchain data processing system using Apache Kafka and Apache Spark Streaming.

## Main Components

1. **Topics Creation and Management** - Setting up topic structures for blockchain data
2. **Kafka Producer** - Collecting data from Ethereum blockchain and sending to Kafka
3. **Kafka Consumer** - Receiving and processing data from Kafka
4. **Kafka Streams** - Real-time data stream processing with Kafka Streams API
5. **Spark Streaming** - Advanced analytics on streaming data with Apache Spark

## Installation

1. Install required libraries:
```
pip install -r requirements.txt
```

2. Use the `run.sh` script to install and run the system:
```
# Check environment and create .env file
./run.sh setup
```

3. Or run Kafka and Zookeeper manually (requires Docker):
```
docker-compose up -d
```

## Usage with run.sh

The `run.sh` script provides commands to easily manage the system:

```
# Start Kafka and Zookeeper
./run.sh start-kafka

# Create Kafka topics
./run.sh create-topics

# Run individual components
./run.sh producer   # Run Ethereum blockchain data producer
./run.sh consumer   # Run Kafka consumer
./run.sh streams    # Run Kafka Streams processor
./run.sh spark      # Run Spark Streaming application

# Start all (Kafka + all components)
./run.sh start-all

# Stop all
./run.sh stop-all

# View logs
./run.sh logs

# View help
./run.sh help
```

## Manual Usage

1. Initialize topics:
```
python kafka_admin.py
```

2. Run the producer to collect blockchain data:
```
python eth_producer.py
```

3. Run the consumer to process data:
```
python eth_consumer.py
```

4. Run the Kafka Streams application:
```
python eth_streams.py
```

5. Run the Spark Streaming application:
```
python spark_streaming.py
```

## Data Processing Pipeline

1. **Ethereum Blockchain Data** → The source of all transaction and block data
2. **Kafka Producer** → Fetches data and sends to Kafka topics
3. **Kafka Topics** → Store raw blockchain data (eth_blocks, eth_transactions)
4. **Processing Layer**:
   - **Kafka Consumer** → Basic processing and filtering
   - **Kafka Streams** → Real-time analytics using Kafka Streams API
   - **Spark Streaming** → Advanced analytics and batch processing using Spark

## Spark Streaming Analytics

The Spark Streaming application performs several types of analytics:

1. **High-Value Transaction Detection** - Identifies transactions with large ETH values
2. **Address Volume Analysis** - Tracks transaction volume by address over time
3. **Contract Interaction Analysis** - Monitors smart contract usage
4. **Block Time Analysis** - Analyzes block creation timing and gas usage
5. **Gas Usage Trends** - Tracks gas usage patterns over time

## Configuration

You can customize settings in the `config.yml` file:

- **Kafka topics**: Change names and configuration of topics
- **Ethereum providers**: Configure connection to Ethereum node
- **Processing thresholds**: Modify thresholds to identify high-value transactions

## Ethereum RPC Provider

This system uses [Llama RPC](https://eth.llamarpc.com) as the default RPC provider for Ethereum, allowing you to use it without registering an API key with Infura or Alchemy. You can change the provider in the `config.yml` file or through the `ETH_PROVIDER_URL` environment variable.

## Environment

Default `.env` file:

```
# Direct provider URL - Using LlamaRPC public endpoint
ETH_PROVIDER_URL=https://eth.llamarpc.com

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

## Output and Logs

- **Console Output** - View real-time analytics in the terminal
- **Log Files** - Check `logs/` directory for detailed application logs
- **Data Output** - Find analysis results in the `output/` directory:
  - `output/address_volume/` - Transaction volume by address
  - `output/contract_interactions/` - Smart contract usage data
  - `output/gas_trends/` - Gas usage patterns 