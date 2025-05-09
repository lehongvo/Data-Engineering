#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate mock web access logs for Flink processing
"""

import random
import datetime
import json
import os
import argparse

# Configuration
URLS = [
    "/home", 
    "/products", 
    "/about", 
    "/contact", 
    "/login", 
    "/register", 
    "/checkout", 
    "/profile", 
    "/api/data", 
    "/admin"
]

STATUS_CODES = [
    200, 200, 200, 200, 200,  # More 200s to make them common
    301, 302, 304,            # Redirects and not modified
    400, 401, 403, 404, 429,  # Client errors
    500, 502, 503             # Server errors
]

# IP range generation
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Generate random timestamp within a date range
def generate_random_timestamp(start_time, end_time):
    time_diff = end_time - start_time
    random_seconds = random.randint(0, int(time_diff.total_seconds()))
    return start_time + datetime.timedelta(seconds=random_seconds)

def generate_log_entry(start_time, end_time, abnormal_ips=None):
    # Use abnormal IPs for some percentage of logs to create unusual patterns
    if abnormal_ips and random.random() < 0.2:  # 20% chance of using an abnormal IP
        ip = random.choice(abnormal_ips)
        # Abnormal IPs have higher chance of errors
        status_code = random.choice([200, 400, 401, 403, 404, 500])
    else:
        ip = generate_random_ip()
        status_code = random.choice(STATUS_CODES)
    
    url = random.choice(URLS)
    timestamp = generate_random_timestamp(start_time, end_time)
    
    return {
        "ip": ip,
        "url": url,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "status_code": status_code
    }

def main():
    parser = argparse.ArgumentParser(description='Generate mock web access logs')
    parser.add_argument('--count', type=int, default=1000, help='Number of log entries to generate')
    parser.add_argument('--output', type=str, default='../data/web_logs.json', help='Output file path')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Define time range for log entries (last 24 hours)
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=24)
    
    # Generate some abnormal IPs that will have more error requests
    abnormal_ips = [generate_random_ip() for _ in range(3)]
    print(f"Abnormal IPs (with more errors): {abnormal_ips}")
    
    # Generate log entries
    logs = []
    for _ in range(args.count):
        log_entry = generate_log_entry(start_time, end_time, abnormal_ips)
        logs.append(log_entry)
    
    # Sort logs by timestamp
    logs.sort(key=lambda x: x["timestamp"])
    
    # Write to file
    with open(args.output, 'w') as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')
    
    print(f"Generated {args.count} log entries in {args.output}")

if __name__ == "__main__":
    main() 