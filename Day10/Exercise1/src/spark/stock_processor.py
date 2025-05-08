#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min, count, sum, stddev, window, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from dotenv import load_dotenv

# Initialize findspark to locate Spark installation
findspark.init()

# Load environment variables
load_dotenv()

# Create logs directory if it doesn't exist
os.makedirs("../logs", exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../logs/spark_job.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("stock-market-processor")

class StockMarketProcessor:
    def __init__(self, input_path, output_path, warehouse_jdbc_url, warehouse_properties):
        """Initialize Spark processor for stock market data."""
        logger.info("Initializing Spark Stock Market Processor")
        
        # Initialize paths
        self.input_path = input_path
        self.output_path = output_path
        self.warehouse_jdbc_url = warehouse_jdbc_url
        self.warehouse_properties = warehouse_properties
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_path, exist_ok=True)
        
        # Initialize Spark session
        self.spark = SparkSession.builder \
            .appName("StockMarketProcessor") \
            .config("spark.sql.warehouse.dir", "spark-warehouse") \
            .config("spark.sql.streaming.checkpointLocation", "checkpoint") \
            .getOrCreate()
            
        # Set log level
        self.spark.sparkContext.setLogLevel("WARN")
        
        logger.info(f"Spark session created with application ID: {self.spark.sparkContext.applicationId}")
        
    def define_schema(self):
        """Define schema for stock market data."""
        return StructType([
            StructField("symbol", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("volume", IntegerType(), True),
            StructField("change_percent", DoubleType(), True)
        ])
        
    def process_batch_data(self):
        """Process stock market data in batch mode."""
        logger.info(f"Processing stock market data from {self.input_path}")
        
        try:
            # Read CSV data
            stock_df = self.spark.read \
                .schema(self.define_schema()) \
                .option("header", "true") \
                .csv(self.input_path)
                
            # Convert timestamp string to timestamp type
            stock_df = stock_df.withColumn("event_time", expr("to_timestamp(timestamp)"))
            
            # Show sample data
            logger.info("Sample data:")
            stock_df.show(5, False)
            
            # Calculate daily statistics per stock
            daily_stats = stock_df \
                .groupBy("symbol") \
                .agg(
                    count("*").alias("trade_count"),
                    avg("price").alias("avg_price"),
                    min("price").alias("min_price"),
                    max("price").alias("max_price"),
                    stddev("price").alias("price_stddev"),
                    sum("volume").alias("total_volume"),
                    avg("change_percent").alias("avg_change_percent")
                )
                
            # Show daily statistics
            logger.info("Daily statistics per stock:")
            daily_stats.show()
            
            # Save to CSV
            daily_stats_path = os.path.join(self.output_path, "daily_stats")
            daily_stats.write.mode("overwrite").csv(daily_stats_path)
            logger.info(f"Daily statistics saved to {daily_stats_path}")
            
            # Compute price movement
            price_movement = stock_df \
                .groupBy("symbol") \
                .agg(
                    min("event_time").alias("first_trade_time"),
                    max("event_time").alias("last_trade_time"),
                    min("price").alias("start_price"),
                    max("price").alias("end_price")
                ) \
                .withColumn("price_change", col("end_price") - col("start_price")) \
                .withColumn("change_percentage", (col("price_change") / col("start_price")) * 100)
                
            # Show price movement
            logger.info("Price movement:")
            price_movement.show()
            
            # Save to CSV
            price_movement_path = os.path.join(self.output_path, "price_movement")
            price_movement.write.mode("overwrite").csv(price_movement_path)
            logger.info(f"Price movement saved to {price_movement_path}")
            
            # Save to data warehouse
            self.save_to_warehouse(daily_stats, "stock_daily_stats")
            self.save_to_warehouse(price_movement, "stock_price_movement")
            
            return daily_stats, price_movement
            
        except Exception as e:
            logger.error(f"Error processing batch data: {e}")
            raise
            
    def save_to_warehouse(self, df, table_name):
        """Save DataFrame to data warehouse."""
        try:
            logger.info(f"Saving {table_name} to data warehouse")
            
            df.write \
                .format("jdbc") \
                .option("url", self.warehouse_jdbc_url) \
                .option("dbtable", table_name) \
                .option("user", self.warehouse_properties["user"]) \
                .option("password", self.warehouse_properties["password"]) \
                .mode("overwrite") \
                .save()
                
            logger.info(f"Successfully saved {table_name} to data warehouse")
        except Exception as e:
            logger.error(f"Error saving to data warehouse: {e}")
            raise
            
    def stop(self):
        """Stop Spark session."""
        if self.spark:
            self.spark.stop()
            logger.info("Spark session stopped")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("../logs", exist_ok=True)
    
    # Get parameters from environment or use defaults
    input_path = os.getenv('INPUT_PATH', '../data')
    output_path = os.getenv('OUTPUT_PATH', '../output')
    
    # Data warehouse connection
    warehouse_jdbc_url = os.getenv('WAREHOUSE_JDBC_URL', 'jdbc:postgresql://localhost:5433/datawarehouse')
    warehouse_properties = {
        "user": os.getenv('WAREHOUSE_USER', 'datauser'),
        "password": os.getenv('WAREHOUSE_PASSWORD', 'datapass'),
        "driver": "org.postgresql.Driver"
    }
    
    try:
        processor = StockMarketProcessor(
            input_path=input_path,
            output_path=output_path,
            warehouse_jdbc_url=warehouse_jdbc_url,
            warehouse_properties=warehouse_properties
        )
        
        processor.process_batch_data()
        
    except Exception as e:
        logger.error(f"Failed to run Spark processor: {e}")
    finally:
        if 'processor' in locals():
            processor.stop() 