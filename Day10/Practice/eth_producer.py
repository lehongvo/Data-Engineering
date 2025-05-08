#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import logging
import os
from datetime import datetime
from decimal import Decimal
from kafka import KafkaProducer
from dotenv import load_dotenv
from utils import load_config, get_web3_provider, format_block_data, format_transaction_data, setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging('eth-producer')

# Custom JSON encoder to handle Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class EthereumProducer:
    def __init__(self, config):
        """Initialize Ethereum producer with Kafka connection and Web3 provider."""
        self.config = config
        self.kafka_bootstrap_servers = config['kafka']['bootstrap_servers']
        self.topics = config['kafka']['topics']
        self.polling_interval = config['ethereum']['polling_interval']
        
        # Initialize Kafka producer with custom JSON encoder
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, cls=DecimalEncoder).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None
        )
        
        # Initialize Web3 provider
        self.w3 = get_web3_provider()
        if not self.w3.is_connected():
            logger.error("Failed to connect to Ethereum node")
            raise ConnectionError("Could not connect to Ethereum node")
        
        logger.info(f"Connected to Ethereum node: {self.w3.client_version}")
        
        # Track the last processed block
        self.last_block_number = self.w3.eth.block_number
        logger.info(f"Starting from block number: {self.last_block_number}")

    def send_to_kafka(self, topic, key, data):
        """Send data to Kafka topic."""
        future = self.producer.send(topic, key=key, value=data)
        try:
            future.get(timeout=10)
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {e}")
            return False
        return True

    def process_transactions(self, transactions, block_number):
        """Process and send block transactions to Kafka."""
        for tx in transactions:
            try:
                # Convert transaction to serializable format using utility
                tx_data = format_transaction_data(tx, self.w3)
                
                # Send transaction data to Kafka
                self.send_to_kafka(self.topics['eth_transactions'], tx_data['hash'], tx_data)
            except Exception as e:
                logger.error(f"Error processing transaction: {e}")
    
    def fetch_and_send_block(self, block_number):
        """Fetch block data and send to Kafka."""
        try:
            # Get block with full transaction details
            block = self.w3.eth.get_block(block_number, full_transactions=True)
            
            # Convert block to serializable format using utility
            block_data = format_block_data(block)
            # Add datetime for convenience
            block_data['datetime'] = datetime.fromtimestamp(block.timestamp).isoformat()
            
            # Send block data to Kafka
            self.send_to_kafka(self.topics['eth_blocks'], block.number, block_data)
            logger.info(f"Sent block {block.number} to Kafka")
            
            # Process transactions in the block
            self.process_transactions(block.transactions, block_number)
            
            return True
        except Exception as e:
            logger.error(f"Error fetching block {block_number}: {e}")
            return False


    def start_streaming(self):
        """Start streaming Ethereum blockchain data to Kafka."""
        logger.info("Starting Ethereum blockchain data streaming...")
        
        while True:
            try:
                current_block = self.w3.eth.block_number
                
                if current_block > self.last_block_number:
                    logger.info(f"New blocks found: {self.last_block_number + 1} to {current_block}")
                    
                    # Process new blocks
                    for block_num in range(self.last_block_number + 1, current_block + 1):
                        success = self.fetch_and_send_block(block_num)
                        if success:
                            self.last_block_number = block_num
                
                # Sleep before next polling
                time.sleep(self.polling_interval)
            except Exception as e:
                logger.error(f"Error in streaming loop: {e}")
                time.sleep(self.polling_interval)

    def close(self):
        """Clean up resources."""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")

if __name__ == "__main__":
    try:
        config = load_config()
        producer = EthereumProducer(config)
        producer.start_streaming()
    except KeyboardInterrupt:
        logger.info("Stopping Ethereum producer...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        if 'producer' in locals():
            producer.close() 