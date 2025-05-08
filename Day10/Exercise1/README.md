# End-to-End Data Pipeline with Kestra, Kafka, and Spark

This project demonstrates a complete data pipeline for processing stock market data using Kestra for orchestration, Kafka for real-time data streaming, and Spark for batch processing. The processed data is stored in a PostgreSQL data warehouse.

## Architecture Overview

```
Stock Data Generator → Kafka → Consumer → CSV Files → Spark Processing → Data Warehouse
             └─────────────────┬────────────────────────────────┘
                               │
                            Kestra
                        (Orchestration)
```

## Components

1. **Kestra**: Workflow orchestration platform that coordinates all the data pipeline steps
2. **Kafka**: Distributed streaming platform for real-time data ingestion
3. **Spark**: Big data processing engine for data transformation and analysis
4. **PostgreSQL**: Data warehouse for storing the processed data

## Directory Structure

```
Exercise1/
├── config/                # Configuration files
├── data/                  # Raw data and Kafka/Zookeeper volumes
├── logs/                  # Application and service logs
├── output/                # Spark output files
├── screenshots/           # Screenshots of the UI components
├── src/                   # Source code
│   ├── kafka/             # Kafka producer and consumer scripts
│   ├── kestra/            # Kestra workflow definitions
│   │   └── flows/         # YAML files defining workflow tasks
│   └── spark/             # Spark processing jobs
├── docker-compose.yml     # Docker services configuration
└── requirements.txt       # Python dependencies
```

## Prerequisites

- Docker and Docker Compose
- Python 3.8 or higher
- Java 11 (for Spark)

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd Exercise1
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Docker services:

```bash
docker-compose up -d
```

This will start:
- Zookeeper (port 2181)
- Kafka (port 9092)
- Kafka UI (port 8080)
- Kestra (port 8090)
- PostgreSQL for Kestra (port 5432)
- PostgreSQL for Data Warehouse (port 5433)

4. Create necessary directories:

```bash
mkdir -p data/zookeeper/data data/zookeeper/log data/kafka/data data/postgres data/warehouse data/kestra/storage logs output
```

## Running the Pipeline

### Option 1: Running via Kestra UI

1. Access Kestra UI at http://localhost:8090
2. Upload the workflow file from `src/kestra/flows/stock_market_pipeline.yml`
3. Execute the workflow from the UI

### Option 2: Running Components Individually

1. Start Kafka and create the topic:

```bash
docker-compose up -d kafka
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create --if-not-exists --topic stock-market-data --partitions 1 --replication-factor 1
```

2. Run the Kafka producer:

```bash
cd src/kafka
python producer.py
```

3. Run the Kafka consumer:

```bash
cd src/kafka
python consumer.py
```

4. Run the Spark processing job:

```bash
cd src/spark
python stock_processor.py
```

## Monitoring and Viewing Results

- **Kestra UI**: http://localhost:8090 - View workflow execution
- **Kafka UI**: http://localhost:8080 - Monitor Kafka topics and messages
- **CSV Data**: Check `data/` directory for raw CSV files
- **Spark Output**: Check `output/` directory for processed data files
- **Data Warehouse**: Connect to PostgreSQL on port 5433

```bash
# View data in warehouse
docker-compose exec data-warehouse psql -U datauser -d datawarehouse -c "SELECT * FROM stock_daily_stats LIMIT 5;"
```

## Log Files

- **Kafka Producer**: `logs/kafka_producer.log`
- **Kafka Consumer**: `logs/kafka_consumer.log`
- **Spark Job**: `logs/spark_job.log`
- **Kestra**: Available through the Kestra UI

## Expected Screenshots

The `screenshots/` directory should contain:
1. Kestra UI showing workflow execution
2. Kafka UI showing topics and messages
3. Spark UI showing job execution
4. Data warehouse query results

## Troubleshooting

1. **Kafka Connection Issues**:
   - Ensure Kafka is running: `docker-compose ps`
   - Check logs: `docker-compose logs kafka`

2. **Spark Processing Errors**:
   - Check Spark logs: `cat logs/spark_job.log`
   - Ensure PostgreSQL JDBC driver is in the classpath

3. **Kestra Workflow Failures**:
   - Check task logs in Kestra UI
   - Ensure paths in workflow YAML are correct

## License

This project is for educational purposes.

## References

- [Kestra Documentation](https://kestra.io/docs)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Spark Documentation](https://spark.apache.org/docs/latest/) 