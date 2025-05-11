#!/bin/bash
set -e

# 1. Start Docker Compose (Kafka, Zookeeper, Schema Registry)
echo "[1/4] Starting Kafka, Zookeeper, and Schema Registry with docker-compose..."
docker-compose up -d

# 2. Create Python virtual environment if not exists
echo "[2/4] Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# 3. Install Python dependencies
echo "[3/4] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run producer and consumer (in background)
echo "[4/4] Running Avro producer and consumer..."
python code/producer_avro.py &
PRODUCER_PID=$!
sleep 2
python code/consumer_avro.py &
CONSUMER_PID=$!

wait $PRODUCER_PID
# Consumer will keep running, so we let it run for a while then kill it
echo "Letting consumer run for 10 seconds..."
sleep 10
kill $CONSUMER_PID || true

# 5. Save Docker logs to log directory
echo "[5/5] Saving Docker logs to log directory..."
mkdir -p log
docker-compose logs kafka > log/kafka.log
docker-compose logs zookeeper > log/zookeeper.log
docker-compose logs schema-registry > log/schema-registry.log

echo "All done! Check output above and logs in the log directory."
