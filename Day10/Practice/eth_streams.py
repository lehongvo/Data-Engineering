#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import time
import threading
from confluent_kafka import Producer, Consumer, TopicPartition
from collections import defaultdict
from utils import load_config, setup_logging

# Setup logging
logger = setup_logging('eth-streams')

class EthereumStreamProcessor:
    def __init__(self, config):
        """Initialize Ethereum stream processor."""
        self.config = config
        self.kafka_bootstrap_servers = config['kafka']['bootstrap_servers']
        self.topics = config['kafka']['topics']
        self.consumer_group = f"{config['kafka']['consumer_group']}-streams"
        
        # State stores
        self.block_stats = {}
        self.address_transaction_counts = defaultdict(int)
        self.high_value_addresses = set()
        
        # Internal flags
        self.running = True
        
        # Kafka consumer and producer configs
        self.consumer_conf = {
            'bootstrap.servers': self.kafka_bootstrap_servers,
            'group.id': self.consumer_group,
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True,
            'auto.commit.interval.ms': 5000
        }
        
        self.producer_conf = {
            'bootstrap.servers': self.kafka_bootstrap_servers
        }
        
        # Create Kafka consumer for transactions
        self.tx_consumer = Consumer(self.consumer_conf)
        self.tx_consumer.subscribe([self.topics['eth_transactions']])
        
        # Create Kafka producer for processed results
        self.producer = Producer(self.producer_conf)

    def delivery_report(self, err, msg):
        """Callback for produced messages."""
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def process_transactions_stream(self):
        """Process Ethereum transactions as a stream."""
        logger.info(f"Starting transaction stream processor")
        
        # State for time windows
        time_window_tx_counts = defaultdict(int)
        last_window_time = int(time.time() // 60) * 60  # 1-minute window
        
        while self.running:
            try:
                msg = self.tx_consumer.poll(1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue
                
                # Process transaction
                tx_data = json.loads(msg.value().decode('utf-8'))
                
                # 1. Analyze by address
                from_address = tx_data.get('from')
                to_address = tx_data.get('to')
                
                if from_address:
                    self.address_transaction_counts[from_address] += 1
                
                if to_address:
                    self.address_transaction_counts[to_address] += 1
                
                # 2. Detect high-activity addresses
                if from_address and self.address_transaction_counts[from_address] > 10:
                    self.high_value_addresses.add(from_address)
                    
                # 3. Calculate within time window (1 minute)
                current_window = int(time.time() // 60) * 60
                if current_window > last_window_time:
                    # Send results of previous window
                    window_results = {
                        'window_start': last_window_time,
                        'window_end': last_window_time + 60,
                        'transaction_count': time_window_tx_counts[last_window_time],
                        'timestamp': int(time.time())
                    }
                    
                    # Export results to Kafka
                    self.producer.produce(
                        'ethereum-transaction-windows',
                        key=str(last_window_time).encode('utf-8'),
                        value=json.dumps(window_results).encode('utf-8'),
                        callback=self.delivery_report
                    )
                    
                    # Update time window
                    last_window_time = current_window
                
                # Increment transaction count for current window
                time_window_tx_counts[current_window] += 1
                
                # 4. Detect suspicious transactions
                if self.is_suspicious_transaction(tx_data):
                    tx_data['suspicious'] = True
                    tx_data['detection_timestamp'] = int(time.time())
                    
                    self.producer.produce(
                        'ethereum-suspicious-transactions',
                        key=tx_data['hash'].encode('utf-8'),
                        value=json.dumps(tx_data).encode('utf-8'),
                        callback=self.delivery_report
                    )
                
                # Periodically flush producer
                self.producer.poll(0)
                
            except Exception as e:
                logger.error(f"Error processing transaction stream: {e}")
        
        # Final flush
        self.producer.flush()

    def is_suspicious_transaction(self, tx_data):
        """Detect suspicious transactions based on multiple factors."""
        # Simple criteria to identify suspicious transactions:
        # 1. High value (> 10 ETH)
        # 2. To a new address (not many previous transactions)
        # 3. Using unusual gas price
        
        suspicious = False
        
        if tx_data.get('value', 0) > 10:  # More than 10 ETH
            to_address = tx_data.get('to')
            if to_address and self.address_transaction_counts[to_address] <= 1:
                # Sending large value to a new address
                suspicious = True
            
            # Unusually low gas price for high-value transaction
            if tx_data.get('gas_price', 0) < 5:  # Less than 5 gwei
                suspicious = True
                
        return suspicious

    def start(self):
        """Start all stream processing tasks."""
        logger.info("Starting Ethereum stream processor...")
        
        # Start the streams in separate threads
        tx_thread = threading.Thread(target=self.process_transactions_stream)
        tx_thread.start()
        
        try:
            # Keep main thread running
            while self.running:
                # Print some stats every 30 seconds
                self.print_stats()
                time.sleep(30)
        except KeyboardInterrupt:
            logger.info("Shutting down stream processor...")
            self.running = False
            
        # Join threads
        tx_thread.join()
        self.close()

    def print_stats(self):
        """Print current statistics."""
        logger.info(f"Monitoring {len(self.address_transaction_counts)} unique addresses")
        logger.info(f"Detected {len(self.high_value_addresses)} high-activity addresses")

    def close(self):
        """Clean up resources."""
        if hasattr(self, 'tx_consumer'):
            self.tx_consumer.close()
            logger.info("Transactions consumer closed")
        
        if hasattr(self, 'producer'):
            self.producer.flush()
            logger.info("Producer flushed and closed")

if __name__ == "__main__":
    try:
        config = load_config()
        processor = EthereumStreamProcessor(config)
        processor.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        if 'processor' in locals():
            processor.close() 