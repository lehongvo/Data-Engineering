#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from utils import load_config, setup_logging

# Setup logging
logger = setup_logging('kafka-admin')

def create_topics(config):
    """Create required Kafka topics if they don't exist."""
    admin_client = KafkaAdminClient(
        bootstrap_servers=config['kafka']['bootstrap_servers'],
        client_id='ethereum-admin'
    )
    
    # Lấy danh sách topics hiện có
    existing_topics = admin_client.list_topics()
    logger.info(f"Existing topics: {existing_topics}")
    
    # Định nghĩa các topics cần thiết
    topic_list = []
    topics_config = config['kafka']['topics']
    
    for topic_name in topics_config.values():
        if topic_name not in existing_topics:
            topic_list.append(NewTopic(
                name=topic_name,
                num_partitions=3,  # multiple partitions for parallelism
                replication_factor=1  # set to 3 in production
            ))
    
    # Tạo thêm các topics cho stream processing
    stream_topics = [
        'ethereum-transaction-windows',
        'ethereum-suspicious-transactions'
    ]
    
    for topic_name in stream_topics:
        if topic_name not in existing_topics:
            topic_list.append(NewTopic(
                name=topic_name,
                num_partitions=3,
                replication_factor=1
            ))
    
    # Tạo các topics nếu cần
    if topic_list:
        try:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            logger.info(f"Successfully created topics: {[t.name for t in topic_list]}")
        except TopicAlreadyExistsError:
            logger.warning("Some topics already exist")
        except Exception as e:
            logger.error(f"Error creating topics: {e}")
    else:
        logger.info("All required topics already exist")
    
    admin_client.close()

if __name__ == "__main__":
    logger.info("Starting Kafka topic administration...")
    config = load_config()
    create_topics(config)
    logger.info("Kafka topic administration completed") 