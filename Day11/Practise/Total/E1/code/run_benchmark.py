#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Benchmark script to compare performance between Apache Flink and Kafka Streams
for processing sales data and calculating hourly revenue by product category
"""

import os
import json
import time
import argparse
import subprocess
import logging
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BenchmarkScript")

def generate_sales_data(count=1000000, output_path="../data/sales_data.json", days=7):
    """Generate sales data for benchmarking."""
    logger.info(f"Generating {count} sales records...")
    
    start_time = time.time()
    
    cmd = [
        "python", "generate_sales_data.py",
        "--count", str(count),
        "--output", output_path,
        "--days", str(days)
    ]
    
    subprocess.run(cmd, check=True)
    
    elapsed = time.time() - start_time
    logger.info(f"Data generation completed in {elapsed:.2f} seconds")
    
    # Verify the file exists and return its size
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        logger.info(f"Generated file size: {size_mb:.2f} MB")
        return size_mb
    else:
        logger.error(f"Failed to generate data file at {output_path}")
        return 0

def run_flink_analysis(input_path, output_path, parallelism=1):
    """Run the Apache Flink sales analysis."""
    logger.info(f"Running Apache Flink sales analysis with parallelism={parallelism}...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cmd = [
        "python", "flink/sales_analysis.py",
        "--input", input_path,
        "--output", output_path,
        "--parallelism", str(parallelism)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        logger.info("Flink analysis completed successfully")
        
        # Load and return metrics
        metrics_file = os.path.join(os.path.dirname(output_path), "flink_metrics.json")
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                return json.load(f)
        else:
            logger.error(f"Metrics file not found: {metrics_file}")
            return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Flink analysis failed: {e}")
        return None

def run_kafka_analysis(input_path, output_path, bootstrap_servers="localhost:9092"):
    """Run the Kafka Streams sales analysis."""
    logger.info("Running Kafka sales analysis...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cmd = [
        "python", "kafka/sales_analysis.py",
        "--input", input_path,
        "--output", output_path,
        "--bootstrap-servers", bootstrap_servers
    ]
    
    try:
        subprocess.run(cmd, check=True)
        logger.info("Kafka analysis completed successfully")
        
        # Load and return metrics
        metrics_file = os.path.join(os.path.dirname(output_path), "kafka_metrics.json")
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                return json.load(f)
        else:
            logger.error(f"Metrics file not found: {metrics_file}")
            return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Kafka analysis failed: {e}")
        return None

def plot_comparison(metrics, output_path="../data/results/comparison.png"):
    """Create a comparison plot of Flink vs Kafka performance."""
    logger.info("Creating performance comparison plot...")
    
    frameworks = [m["framework"] for m in metrics]
    execution_times = [m["execution_time_seconds"] for m in metrics]
    
    # Create a pandas DataFrame for better visualization
    df = pd.DataFrame({
        "Framework": frameworks,
        "Execution Time (seconds)": execution_times
    })
    
    # Create plot directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Plot bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df["Framework"], df["Execution Time (seconds)"], color=["#6baed6", "#fd8d3c"])
    
    # Add values on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f"{height:.2f}s", ha='center', va='bottom', fontweight='bold')
    
    plt.title("Performance Comparison: Apache Flink vs Kafka", fontsize=16)
    plt.ylabel("Execution Time (seconds)", fontsize=14)
    plt.xlabel("Framework", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_path)
    logger.info(f"Comparison plot saved to {output_path}")
    
    # Print textual comparison
    fastest = min(metrics, key=lambda x: x["execution_time_seconds"])
    slowest = max(metrics, key=lambda x: x["execution_time_seconds"])
    
    speed_diff = slowest["execution_time_seconds"] / fastest["execution_time_seconds"]
    
    print("\n" + "="*50)
    print(f"PERFORMANCE COMPARISON RESULTS")
    print("="*50)
    print(f"Fastest: {fastest['framework']} - {fastest['execution_time_seconds']:.2f} seconds")
    print(f"Slowest: {slowest['framework']} - {slowest['execution_time_seconds']:.2f} seconds")
    print(f"{fastest['framework']} is {speed_diff:.2f}x faster than {slowest['framework']}")
    print("="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Benchmark Apache Flink vs Kafka Streams")
    parser.add_argument("--data-count", type=int, default=1000000,
                      help="Number of sales records to generate (default: 1,000,000)")
    parser.add_argument("--data-path", type=str, default="../data/sales_data.json",
                      help="Path to save/load sales data")
    parser.add_argument("--generate-data", action="store_true",
                      help="Generate new sales data (if not provided, uses existing data)")
    parser.add_argument("--parallelism", type=int, default=1,
                      help="Parallelism level for processing (default: 1)")
    parser.add_argument("--output-dir", type=str, default="../data/results",
                      help="Output directory for results")
    
    args = parser.parse_args()
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(args.output_dir, f"benchmark_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    
    # Step 1: Generate or use existing data
    if args.generate_data or not os.path.exists(args.data_path):
        data_size_mb = generate_sales_data(args.data_count, args.data_path)
    else:
        data_size_mb = os.path.getsize(args.data_path) / (1024 * 1024)
        logger.info(f"Using existing data file: {args.data_path} ({data_size_mb:.2f} MB)")
    
    # Step 2: Run Flink analysis
    flink_output = os.path.join(run_dir, "flink")
    flink_metrics = run_flink_analysis(args.data_path, flink_output, args.parallelism)
    
    # Step 3: Run Kafka analysis
    kafka_output = os.path.join(run_dir, "kafka")
    kafka_metrics = run_kafka_analysis(args.data_path, kafka_output)
    
    # Step 4: Compare and visualize results
    if flink_metrics and kafka_metrics:
        # Add data size to metrics
        flink_metrics["data_size_mb"] = data_size_mb
        kafka_metrics["data_size_mb"] = data_size_mb
        
        # Plot comparison
        plot_comparison([flink_metrics, kafka_metrics], os.path.join(run_dir, "comparison.png"))
        
        # Save combined metrics
        combined_metrics = {
            "timestamp": timestamp,
            "data_size_mb": data_size_mb,
            "record_count": args.data_count,
            "frameworks": [flink_metrics, kafka_metrics]
        }
        
        with open(os.path.join(run_dir, "benchmark_results.json"), 'w') as f:
            json.dump(combined_metrics, f, indent=2)
        
        logger.info(f"Benchmark completed. Results saved to {run_dir}")
    else:
        logger.error("Benchmark failed: Could not get metrics from one or both frameworks")

if __name__ == "__main__":
    main() 