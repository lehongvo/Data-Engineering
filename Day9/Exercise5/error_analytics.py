#!/usr/bin/env python3
import json
import logging
import sys
import time
from datetime import datetime
from collections import defaultdict, Counter
from prettytable import PrettyTable
from kafka import KafkaConsumer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("error_analytics.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("error-analytics")

# Global variables to track statistics
total_errors = 0
error_types = Counter()
error_by_sensor = defaultdict(Counter)
validation_errors = Counter()
error_history = []  # Store error statistics history to analyze trends

# Create consumer to read from error-analytics topic
try:
    consumer = KafkaConsumer(
        'error-analytics',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='error-analytics-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Successfully connected to Kafka error-analytics topic")
except Exception as e:
    logger.error(f"Cannot connect to Kafka: {e}")
    sys.exit(1)

def print_error_summary():
    """Print error overview"""
    logger.info("=== ERROR SUMMARY REPORT ===")
    logger.info(f"Total errors detected: {total_errors}")
    
    # Create error type table
    table = PrettyTable()
    table.field_names = ["Error Type", "Count", "Percentage %"]
    
    for error_type, count in error_types.most_common():
        percentage = 0 if total_errors == 0 else count * 100 / total_errors
        table.add_row([error_type, count, f"{percentage:.2f}%"])
    
    logger.info("TOP ERROR TYPES:")
    logger.info("\n" + str(table))

def print_sensor_error_summary():
    """Print error statistics by sensor"""
    if not error_by_sensor:
        return
    
    logger.info("=== ERRORS BY SENSOR ===")
    
    # Create table of errors by device
    table = PrettyTable()
    table.field_names = ["Sensor ID", "Total Errors", "Most Common Error"]
    
    for sensor_id, errors in sorted(error_by_sensor.items(), 
                                   key=lambda x: sum(x[1].values()), 
                                   reverse=True):
        total = sum(errors.values())
        most_common = errors.most_common(1)
        most_common_error = most_common[0][0] if most_common else "N/A"
        table.add_row([sensor_id, total, most_common_error])
    
    logger.info("\n" + str(table))

def print_validation_error_summary():
    """Print detailed validation error statistics"""
    if not validation_errors:
        return
    
    logger.info("=== VALIDATION ERROR DETAILS ===")
    
    # Create validation error table
    table = PrettyTable()
    table.field_names = ["Validation Error", "Count"]
    
    for error, count in validation_errors.most_common():
        table.add_row([error, count])
    
    logger.info("\n" + str(table))

def analyze_error_trends():
    """Analyze error trends over time"""
    if len(error_history) < 2:
        return
    
    # Get current and previous data
    current = error_history[-1]
    previous = error_history[-2]
    
    # Compare total errors
    current_total = current["total_errors"]
    previous_total = previous["total_errors"]
    
    if current_total > previous_total:
        logger.warning(f"Error trend is INCREASING: {previous_total} → {current_total}")
    elif current_total < previous_total:
        logger.info(f"Error trend is DECREASING: {previous_total} → {current_total}")
    
    # Analyze trends by error type (can be expanded)
    logger.info("Notable increasing error types:")
    
    for error_type, count in current["error_counts_by_type"].items():
        prev_count = previous["error_counts_by_type"].get(error_type, 0)
        if count > prev_count * 1.5:  # Increase by more than 50%
            logger.warning(f"- {error_type}: increased from {prev_count} to {count}")

# Process error analytics records from Kafka
try:
    logger.info("Starting to analyze error data from 'error-analytics' topic...")
    report_counter = 0
    
    for message in consumer:
        try:
            analytics = message.value
            report_counter += 1
            
            # Store history for trend analysis
            error_history.append(analytics)
            if len(error_history) > 10:  # Only keep the 10 most recent records
                error_history.pop(0)
            
            # Update statistics
            total_errors = analytics.get("total_errors", 0)
            error_types.update(analytics.get("error_counts_by_type", {}))
            
            # Update errors by sensor
            for sensor_id, counts in analytics.get("error_counts_by_sensor", {}).items():
                error_by_sensor[sensor_id].update(counts)
            
            # Update validation errors
            validation_errors.update(analytics.get("validation_error_types", {}))
            
            # Print periodic reports
            logger.info(f"Received error analysis report #{report_counter}")
            print_error_summary()
            print_sensor_error_summary()
            print_validation_error_summary()
            
            # Analyze trends after at least 2 reports
            if len(error_history) >= 2:
                analyze_error_trends()
            
            logger.info("=" * 80)  # Separator line between reports
            
        except Exception as e:
            logger.error(f"Error processing analytics record: {e}")

except KeyboardInterrupt:
    logger.info("Interrupted by user, stopping error analytics")
except Exception as e:
    logger.error(f"Unidentified error: {e}")
finally:
    try:
        consumer.close()
    except:
        pass
    logger.info("Error Analytics stopped") 