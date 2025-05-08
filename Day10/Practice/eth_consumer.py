#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import time
import threading
from kafka import KafkaConsumer
from kafka import KafkaProducer
from utils import load_config, setup_logging

# Setup logging
logger = setup_logging('eth-consumer')

class EthereumConsumer:
    def __init__(self, config):
        """Initialize Ethereum consumer with Kafka connection."""
        self.config = config
        self.kafka_bootstrap_servers = config['kafka']['bootstrap_servers']
        self.topics = config['kafka']['topics']
        self.consumer_group = config['kafka']['consumer_group']
        self.high_value_threshold = config['processing']['high_value_threshold']
        
        # Initialize Kafka consumers for different topics
        self.block_consumer = self.create_consumer([self.topics['eth_blocks']])
        self.transaction_consumer = self.create_consumer([self.topics['eth_transactions']])
        
        # Initialize Kafka producer for processed data
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None
        )
        
        self.running = True

    def create_consumer(self, topics):
        """Create a Kafka consumer for the specified topics."""
        return KafkaConsumer(
            *topics,
            bootstrap_servers=self.kafka_bootstrap_servers,
            group_id=self.consumer_group,
            auto_offset_reset='latest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda m: m.decode('utf-8') if m else None,
            enable_auto_commit=True,
            auto_commit_interval_ms=5000
        )

    def process_blocks(self):
        """Process Ethereum blocks from Kafka topic."""
        logger.info(f"Starting block consumer for topic: {self.topics['eth_blocks']}")
        
        for message in self.block_consumer:
            if not self.running:
                break
                
            try:
                block_data = message.value
                logger.info(f"Processing block #{block_data['number']} with {block_data['transaction_count']} transactions")
                
                # Ở đây có thể thêm logic xử lý block
                # Ví dụ: Phân tích khối lượng giao dịch, gas used, etc.
                
                # In thông tin tóm tắt về block
                print(f"Block #{block_data['number']} | Time: {block_data['datetime']} | Tx Count: {block_data['transaction_count']} | Gas Used: {block_data['gas_used']}")
                
            except Exception as e:
                logger.error(f"Error processing block: {e}")

    def process_transactions(self):
        """Process Ethereum transactions from Kafka topic and identify high-value transactions."""
        logger.info(f"Starting transaction consumer for topic: {self.topics['eth_transactions']}")
        
        for message in self.transaction_consumer:
            if not self.running:
                break
                
            try:
                tx_data = message.value
                
                # Lọc các giao dịch có giá trị cao
                if self.is_high_value_transaction(tx_data):
                    self.producer.send(
                        self.topics['high_value_transactions'],
                        key=tx_data['hash'],
                        value=tx_data
                    )
                    logger.info(f"High-value transaction detected: {tx_data['hash']} - {tx_data['value']} ETH")
                    
                # Phân tích dữ liệu giao dịch
                self.analyze_transaction(tx_data)
                
            except Exception as e:
                logger.error(f"Error processing transaction: {e}")

    def is_high_value_transaction(self, tx_data):
        """Check if transaction is high-value based on threshold."""
        return tx_data.get('value', 0) >= self.high_value_threshold

    def analyze_transaction(self, tx_data):
        """Analyze transaction data for insights."""
        try:
            # Phân loại loại giao dịch (transfer, contract call, etc.)
            # Sử dụng trường đã được thêm bởi producer
            tx_type = tx_data.get('is_contract_call', False)
            tx_type_str = "Contract Call" if tx_type else "ETH Transfer"
            
            # Chỉ in các giao dịch có giá trị để demo (tránh spam console)
            if tx_data.get('value', 0) > 0:
                print(f"Transaction: {tx_data['hash'][:10]}... | Type: {tx_type_str} | Value: {tx_data['value']:.4f} ETH | From: {tx_data['from'][:8]}... | To: {tx_data.get('to', 'Contract Creation')[:8]}...")
                
            # Gửi kết quả phân tích đến Kafka topic
            enriched_data = {
                **tx_data,
                'transaction_type': tx_type_str,
                'processed_timestamp': int(time.time())
            }
            
            self.producer.send(
                self.topics['filtered_transactions'],
                key=tx_data['hash'],
                value=enriched_data
            )
                
        except Exception as e:
            logger.error(f"Error analyzing transaction: {e}")

    def start(self):
        """Start consuming and processing Ethereum data."""
        logger.info("Starting Ethereum data consumers...")
        
        # Start processing in separate threads
        block_thread = threading.Thread(target=self.process_blocks)
        transaction_thread = threading.Thread(target=self.process_transactions)
        
        block_thread.start()
        transaction_thread.start()
        
        try:
            # Keep main thread running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down consumers...")
            self.running = False
            
        # Join threads
        block_thread.join()
        transaction_thread.join()
        
        self.close()

    def close(self):
        """Clean up resources."""
        if hasattr(self, 'block_consumer'):
            self.block_consumer.close()
            logger.info("Block consumer closed")
            
        if hasattr(self, 'transaction_consumer'):
            self.transaction_consumer.close()
            logger.info("Transaction consumer closed")
            
        if hasattr(self, 'producer'):
            self.producer.flush()
            self.producer.close()
            logger.info("Producer closed")

if __name__ == "__main__":
    try:
        config = load_config()
        consumer = EthereumConsumer(config)
        consumer.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close() 