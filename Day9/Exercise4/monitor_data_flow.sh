#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p logs

# Define log files
POSTGRES_LOG="logs/postgres_changes.log"
KAFKA_TOPICS_LOG="logs/kafka_topics.log"
KAFKA_MESSAGES_LOG="logs/kafka_messages.log"
MONGODB_LOG="logs/mongodb_changes.log"
SYSTEM_LOG="logs/system_flow.log"

# Clear old logs if they exist
> $POSTGRES_LOG
> $KAFKA_TOPICS_LOG
> $KAFKA_MESSAGES_LOG
> $MONGODB_LOG
> $SYSTEM_LOG

echo "========================================" | tee -a $SYSTEM_LOG
echo "Starting data flow logging: $(date)" | tee -a $SYSTEM_LOG
echo "========================================" | tee -a $SYSTEM_LOG

# Check and log Kafka topics
echo "Current Kafka topics:" | tee -a $KAFKA_TOPICS_LOG
docker-compose exec -T kafka kafka-topics.sh --list --bootstrap-server kafka:9092 | tee -a $KAFKA_TOPICS_LOG
echo "----------------------------------------" | tee -a $KAFKA_TOPICS_LOG

# Check tables in PostgreSQL
echo "Initial data in PostgreSQL:" | tee -a $POSTGRES_LOG
echo "-- customers table:" | tee -a $POSTGRES_LOG
docker-compose exec -T postgres psql -U postgres -d kafkaconnect -c 'SELECT * FROM customers;' | tee -a $POSTGRES_LOG
echo "-- products table:" | tee -a $POSTGRES_LOG
docker-compose exec -T postgres psql -U postgres -d kafkaconnect -c 'SELECT * FROM products;' | tee -a $POSTGRES_LOG
echo "-- orders table:" | tee -a $POSTGRES_LOG
docker-compose exec -T postgres psql -U postgres -d kafkaconnect -c 'SELECT * FROM orders;' | tee -a $POSTGRES_LOG
echo "----------------------------------------" | tee -a $POSTGRES_LOG

# Check collections in MongoDB
echo "Initial data in MongoDB:" | tee -a $MONGODB_LOG
echo "-- customers collection:" | tee -a $MONGODB_LOG
docker-compose exec -T mongodb mongosh --quiet --username root --password example --authenticationDatabase admin kafkaconnect --eval 'db.customers.find().toArray()' | tee -a $MONGODB_LOG
echo "-- products collection:" | tee -a $MONGODB_LOG
docker-compose exec -T mongodb mongosh --quiet --username root --password example --authenticationDatabase admin kafkaconnect --eval 'db.products.find().toArray()' | tee -a $MONGODB_LOG
echo "-- orders collection:" | tee -a $MONGODB_LOG
docker-compose exec -T mongodb mongosh --quiet --username root --password example --authenticationDatabase admin kafkaconnect --eval 'db.orders.find().toArray()' | tee -a $MONGODB_LOG
echo "----------------------------------------" | tee -a $MONGODB_LOG

# Add new data to PostgreSQL to trigger data flow
echo -e "\nAdding new data to PostgreSQL to trigger data flow:" | tee -a $SYSTEM_LOG
docker-compose exec -T postgres psql -U postgres -d kafkaconnect -c "INSERT INTO customers (name, email) VALUES ('Data Flow Customer', 'dataflow@example.com');" | tee -a $POSTGRES_LOG

# Wait for data to be processed
echo "Waiting 10 seconds for data to flow through Kafka..." | tee -a $SYSTEM_LOG
sleep 10

# Check for new data in topics
echo -e "\nChecking Kafka topics after adding data:" | tee -a $KAFKA_TOPICS_LOG
docker-compose exec -T kafka kafka-topics.sh --list --bootstrap-server kafka:9092 | tee -a $KAFKA_TOPICS_LOG

# Check topic content (if any)
TOPICS=$(docker-compose exec -T kafka kafka-topics.sh --list --bootstrap-server kafka:9092)
for topic in $TOPICS; do
  if [[ $topic == *"customers"* ]]; then
    echo -e "\nMessages in topic '$topic':" | tee -a $KAFKA_MESSAGES_LOG
    docker-compose exec -T kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic $topic --from-beginning --max-messages 5 | tee -a $KAFKA_MESSAGES_LOG
  fi
done

# Check for new data in MongoDB
echo -e "\nChecking for new data in MongoDB after adding to PostgreSQL:" | tee -a $MONGODB_LOG
docker-compose exec -T mongodb mongosh --quiet --username root --password example --authenticationDatabase admin kafkaconnect --eval 'db.customers.find({email: "dataflow@example.com"}).toArray()' | tee -a $MONGODB_LOG

# Summary of results
echo -e "\n========================================" | tee -a $SYSTEM_LOG
echo "Data flow logging results: $(date)" | tee -a $SYSTEM_LOG
echo "- PostgreSQL log: $POSTGRES_LOG" | tee -a $SYSTEM_LOG
echo "- Kafka topics log: $KAFKA_TOPICS_LOG" | tee -a $SYSTEM_LOG
echo "- Kafka messages log: $KAFKA_MESSAGES_LOG" | tee -a $SYSTEM_LOG
echo "- MongoDB log: $MONGODB_LOG" | tee -a $SYSTEM_LOG
echo "========================================" | tee -a $SYSTEM_LOG

echo "Data flow logging completed. See log files in the 'logs/' directory." 