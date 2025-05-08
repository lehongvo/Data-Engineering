# Exercise 6: Comprehensive Data Engineering Project with Infrastructure as Code
# This script simulates a complete data engineering project with:
# 1. Infrastructure setup using Docker and Terraform
# 2. Implementation of batch and streaming data pipelines
# 3. Project management and documentation

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_json, struct, window, count, sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType
import os
import json
import socket
import time
import subprocess
from datetime import datetime

class DataEngineeringProject:
    def __init__(self):
        self.project_name = "Comprehensive Data Engineering Project"
        self.spark = SparkSession.builder.appName(self.project_name).getOrCreate()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Components status
        self.infrastructure = {
            "docker": self.check_docker_running(),
            "postgres": self.check_service_availability("localhost", 5432),
            "kafka": self.check_service_availability("localhost", 9092),
            "prometheus": self.check_service_availability("localhost", 9090),
            "grafana": self.check_service_availability("localhost", 3000)
        }
        
        # Project structure
        self.project_structure = {
            "infrastructure": ["docker-compose.yml", "terraform/", "monitoring/"],
            "data_pipelines": ["batch_processing/", "stream_processing/", "dbt_transformations/"],
            "documentation": ["architecture.md", "data_models.md", "operations.md"]
        }

    def check_docker_running(self):
        """Check if Docker is running"""
        try:
            result = subprocess.run(["docker", "info"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  text=True, 
                                  check=False)
            return result.returncode == 0
        except:
            return False

    def check_service_availability(self, host, port):
        """Check if a service is available at the specified host and port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def display_project_status(self):
        """Display the status of project components"""
        print("\n" + "="*50)
        print(f"PROJECT STATUS: {self.project_name}")
        print("="*50)
        
        print("\n1. INFRASTRUCTURE STATUS:")
        for component, status in self.infrastructure.items():
            status_text = "RUNNING" if status else "NOT RUNNING"
            print(f"   - {component.upper()}: {status_text}")
        
        print("\n2. PROJECT STRUCTURE:")
        for category, items in self.project_structure.items():
            print(f"   - {category.upper()}:")
            for item in items:
                print(f"     * {item}")
        
        print("\n3. DATA PIPELINES:")
        self.simulate_pipeline_status()
        
        print("\n" + "="*50)
    
    def simulate_pipeline_status(self):
        """Simulate the status of various data pipelines"""
        pipelines = [
            {"name": "Raw Data Ingestion", "type": "batch", "status": "SUCCESS", "last_run": "2023-05-05 23:45:00"},
            {"name": "Customer Analytics", "type": "batch", "status": "SUCCESS", "last_run": "2023-05-06 01:30:00"},
            {"name": "Product Metrics", "type": "batch", "status": "WARNING", "last_run": "2023-05-06 02:15:00"},
            {"name": "User Activity Stream", "type": "streaming", "status": "RUNNING", "uptime": "23h 45m"},
            {"name": "Real-time Alerts", "type": "streaming", "status": "RUNNING", "uptime": "23h 45m"}
        ]
        
        batch_pipelines = [p for p in pipelines if p["type"] == "batch"]
        stream_pipelines = [p for p in pipelines if p["type"] == "streaming"]
        
        print("   BATCH PIPELINES:")
        for p in batch_pipelines:
            print(f"     * {p['name']} - Status: {p['status']} - Last Run: {p['last_run']}")
        
        print("   STREAMING PIPELINES:")
        for p in stream_pipelines:
            print(f"     * {p['name']} - Status: {p['status']} - Uptime: {p['uptime']}")
    
    def simulate_data_processing(self):
        """Simulate batch and streaming data processing with Spark"""
        print("\nSimulating data processing workflows...\n")
        
        # 1. Simulate batch processing
        self.simulate_batch_processing()
        
        # 2. Simulate stream processing
        self.simulate_stream_processing()
    
    def simulate_batch_processing(self):
        """Simulate batch processing with Spark"""
        print("BATCH PROCESSING SIMULATION:")
        
        # Create sample data
        sales_data = [
            (1, "Product A", "Electronics", 10, 1999.99, "2023-05-01"),
            (2, "Product B", "Clothing", 5, 99.95, "2023-05-01"),
            (3, "Product C", "Home", 2, 499.95, "2023-05-01"),
            (4, "Product A", "Electronics", 8, 1999.99, "2023-05-02"),
            (5, "Product D", "Food", 20, 5.99, "2023-05-02"),
            (6, "Product B", "Clothing", 15, 99.95, "2023-05-03"),
            (7, "Product E", "Electronics", 3, 2999.99, "2023-05-03")
        ]
        
        schema = ["order_id", "product_name", "category", "quantity", "price", "order_date"]
        df = self.spark.createDataFrame(sales_data, schema)
        
        # Show the original data
        print("\nSample Sales Data:")
        df.show(5)
        
        # Perform batch transformations
        print("\nBatch Processing - Daily Sales by Category:")
        daily_sales = df.groupBy("order_date", "category").agg(
            count("order_id").alias("order_count"),
            sum(col("price") * col("quantity")).alias("total_revenue")
        ).orderBy("order_date", "category")
        
        daily_sales.show()
        
        print("Batch Processing - Top Categories by Revenue:")
        top_categories = df.groupBy("category").agg(
            sum(col("price") * col("quantity")).alias("total_revenue")
        ).orderBy(col("total_revenue").desc())
        
        top_categories.show()
    
    def simulate_stream_processing(self):
        """Simulate stream processing with Spark Structured Streaming"""
        print("\nSTREAM PROCESSING SIMULATION:")
        
        # Since we're just simulating, we'll create a rate stream
        # In a real project, this would connect to Kafka or another streaming source
        print("Starting simulated event stream (press Ctrl+C to stop)...")
        
        # Create sample events to join with the rate stream
        events = [
            ("page_view", "home", "user1"),
            ("click", "product", "user2"),
            ("add_to_cart", "cart", "user3"),
            ("purchase", "checkout", "user2"),
            ("page_view", "home", "user4")
        ]
        
        events_df = self.spark.createDataFrame(events, ["event_type", "page", "user_id"])
        
        try:
            # Create a stream and join with events
            rate_stream = self.spark.readStream.format("rate").option("rowsPerSecond", 5).load()
            
            # Join with static data for demonstration
            joined_stream = rate_stream.crossJoin(events_df)
            
            # Aggregate events
            windowed_counts = joined_stream \
                .groupBy(window(col("timestamp"), "10 seconds"), "event_type") \
                .count() \
                .orderBy("window", "event_type")
            
            # Show the stream in the console
            query = windowed_counts.writeStream \
                .outputMode("complete") \
                .format("console") \
                .option("truncate", False) \
                .start()
            
            # Run for a short time
            query.awaitTermination(30)
            query.stop()
            
        except Exception as e:
            print(f"Stream processing simulation error: {e}")
    
    def generate_documentation(self):
        """Generate project documentation"""
        print("\nGENERATING PROJECT DOCUMENTATION:")
        
        # 1. Architecture document
        architecture = {
            "title": "System Architecture",
            "overview": "Our data platform uses a lambda architecture with batch and speed layers",
            "components": [
                {"name": "Data Ingest Layer", "technologies": ["Apache Kafka", "Debezium", "Apache NiFi"]},
                {"name": "Storage Layer", "technologies": ["S3/GCS", "PostgreSQL", "Redis"]},
                {"name": "Processing Layer", "technologies": ["Apache Spark", "Apache Flink"]},
                {"name": "Serving Layer", "technologies": ["dbt", "Snowflake", "Redshift"]},
                {"name": "Visualization Layer", "technologies": ["Tableau", "Looker", "Grafana"]}
            ],
            "infrastructure": {
                "provider": "AWS/GCP",
                "deployment": "Terraform, Docker, Kubernetes",
                "monitoring": "Prometheus, Grafana, ELK Stack"
            }
        }
        
        # 2. Data models
        data_models = {
            "sources": ["CRM", "ERP", "Web Analytics", "Mobile App"],
            "raw_tables": ["users_raw", "orders_raw", "events_raw", "products_raw"],
            "transformed_tables": ["dim_users", "dim_products", "fact_orders", "fact_events"],
            "metrics": ["Daily Active Users", "Conversion Rate", "Retention Rate", "Revenue"]
        }
        
        # 3. Operations
        operations = {
            "scheduling": "Airflow",
            "monitoring": "Prometheus + Grafana",
            "alerting": "PagerDuty",
            "disaster_recovery": {
                "backup_frequency": "Daily",
                "retention_period": "30 days",
                "recovery_time_objective": "4 hours"
            },
            "security": {
                "data_encryption": "At rest and in transit",
                "access_control": "Role-based",
                "audit_logging": "All operations logged"
            }
        }
        
        # Print summary of documentation
        print("\nDocumentation Generated:")
        print(f"1. Architecture Document: {len(architecture['components'])} components defined")
        print(f"2. Data Models: {len(data_models['raw_tables'])} raw tables, {len(data_models['transformed_tables'])} transformed tables")
        print(f"3. Operations Manual: Covers {', '.join(operations.keys())}")
    
    def run(self):
        """Run the complete project simulation"""
        self.display_project_status()
        self.simulate_data_processing()
        self.generate_documentation()
        
        print("\n" + "="*50)
        print("PROJECT SIMULATION COMPLETED")
        print("="*50)
        print("\nKey Takeaways:")
        print("1. Infrastructure as Code enables reproducible environments")
        print("2. Combined batch and streaming pipelines provide complete data processing")
        print("3. Documentation is essential for project sustainability")
        print("="*50)

if __name__ == "__main__":
    project = DataEngineeringProject()
    project.run() 