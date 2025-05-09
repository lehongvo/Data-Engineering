#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate sales data for benchmark comparison between Kafka Streams and Flink
"""

import random
import datetime
import json
import os
import argparse
import uuid
from typing import Dict, List, Any

# Configuration for sales data generation
PRODUCT_CATEGORIES = [
    "Electronics", "Clothing", "Home & Kitchen", "Books", "Sports", 
    "Beauty", "Toys", "Automotive", "Grocery", "Health"
]

# Products with price ranges by category
PRODUCTS_BY_CATEGORY = {
    "Electronics": [
        {"name": "Smartphone", "price_range": (300, 1200)},
        {"name": "Laptop", "price_range": (500, 2500)},
        {"name": "Headphones", "price_range": (20, 350)},
        {"name": "Tablet", "price_range": (100, 800)},
        {"name": "Smart Watch", "price_range": (50, 500)}
    ],
    "Clothing": [
        {"name": "T-shirt", "price_range": (10, 50)},
        {"name": "Jeans", "price_range": (20, 150)},
        {"name": "Jacket", "price_range": (30, 300)},
        {"name": "Shoes", "price_range": (25, 200)},
        {"name": "Dress", "price_range": (25, 250)}
    ],
    "Home & Kitchen": [
        {"name": "Blender", "price_range": (30, 200)},
        {"name": "Coffee Maker", "price_range": (20, 500)},
        {"name": "Toaster", "price_range": (15, 150)},
        {"name": "Cookware Set", "price_range": (50, 400)},
        {"name": "Vacuum Cleaner", "price_range": (100, 600)}
    ],
    "Books": [
        {"name": "Fiction", "price_range": (5, 30)},
        {"name": "Non-fiction", "price_range": (10, 50)},
        {"name": "Textbook", "price_range": (30, 150)},
        {"name": "Children's Book", "price_range": (5, 25)},
        {"name": "Cookbook", "price_range": (15, 40)}
    ],
    "Sports": [
        {"name": "Yoga Mat", "price_range": (15, 80)},
        {"name": "Dumbbells", "price_range": (20, 100)},
        {"name": "Sports Shoes", "price_range": (40, 200)},
        {"name": "Tennis Racket", "price_range": (30, 300)},
        {"name": "Bicycle", "price_range": (200, 2000)}
    ],
    "Beauty": [
        {"name": "Lipstick", "price_range": (5, 50)},
        {"name": "Shampoo", "price_range": (5, 30)},
        {"name": "Perfume", "price_range": (20, 150)},
        {"name": "Face Cream", "price_range": (10, 100)},
        {"name": "Makeup Kit", "price_range": (30, 200)}
    ],
    "Toys": [
        {"name": "Action Figure", "price_range": (10, 50)},
        {"name": "Board Game", "price_range": (15, 80)},
        {"name": "Puzzle", "price_range": (10, 40)},
        {"name": "Remote Control Car", "price_range": (20, 150)},
        {"name": "Doll", "price_range": (15, 100)}
    ],
    "Automotive": [
        {"name": "Car Charger", "price_range": (10, 40)},
        {"name": "Dashboard Camera", "price_range": (50, 300)},
        {"name": "Floor Mats", "price_range": (20, 100)},
        {"name": "Car Cover", "price_range": (30, 150)},
        {"name": "Tool Kit", "price_range": (25, 200)}
    ],
    "Grocery": [
        {"name": "Coffee Beans", "price_range": (10, 50)},
        {"name": "Olive Oil", "price_range": (8, 30)},
        {"name": "Pasta", "price_range": (2, 15)},
        {"name": "Chocolate", "price_range": (3, 20)},
        {"name": "Cereal", "price_range": (3, 10)}
    ],
    "Health": [
        {"name": "Vitamins", "price_range": (10, 50)},
        {"name": "Protein Powder", "price_range": (20, 80)},
        {"name": "First Aid Kit", "price_range": (15, 100)},
        {"name": "Digital Thermometer", "price_range": (10, 60)},
        {"name": "Hand Sanitizer", "price_range": (3, 15)}
    ]
}

# Locations for stores
LOCATIONS = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
]

def generate_customer_id() -> str:
    """Generate a random customer ID."""
    return f"cust_{random.randint(1000, 9999)}"

def generate_timestamp(start_time: datetime.datetime, end_time: datetime.datetime) -> str:
    """Generate a random timestamp between start_time and end_time."""
    time_diff = end_time - start_time
    random_seconds = random.randint(0, int(time_diff.total_seconds()))
    timestamp = start_time + datetime.timedelta(seconds=random_seconds)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def generate_product() -> Dict[str, Any]:
    """Generate a random product from a random category."""
    category = random.choice(PRODUCT_CATEGORIES)
    product = random.choice(PRODUCTS_BY_CATEGORY[category])
    price_range = product["price_range"]
    price = round(random.uniform(price_range[0], price_range[1]), 2)
    return {
        "category": category,
        "product_name": product["name"],
        "price": price
    }

def generate_quantity() -> int:
    """Generate a random quantity, with bias towards smaller numbers."""
    weights = [0.5, 0.25, 0.15, 0.05, 0.03, 0.02]
    quantity_options = [1, 2, 3, 4, 5, random.randint(6, 20)]
    return random.choices(quantity_options, weights=weights)[0]

def generate_sale_record() -> Dict[str, Any]:
    """Generate a complete sale record."""
    product_info = generate_product()
    quantity = generate_quantity()
    total_price = round(product_info["price"] * quantity, 2)
    
    return {
        "sale_id": str(uuid.uuid4()),
        "customer_id": generate_customer_id(),
        "location": random.choice(LOCATIONS),
        "product_category": product_info["category"],
        "product_name": product_info["product_name"],
        "price": product_info["price"],
        "quantity": quantity,
        "total_amount": total_price
    }

def generate_sales_data(
    count: int, 
    start_time: datetime.datetime, 
    end_time: datetime.datetime
) -> List[Dict[str, Any]]:
    """Generate a list of sales records within the time range."""
    sales_data = []
    for _ in range(count):
        record = generate_sale_record()
        record["timestamp"] = generate_timestamp(start_time, end_time)
        sales_data.append(record)
    
    # Sort by timestamp
    sales_data.sort(key=lambda x: x["timestamp"])
    return sales_data

def main():
    parser = argparse.ArgumentParser(description='Generate sales data for benchmarking')
    
    parser.add_argument('--count', type=int, default=1000000, 
                        help='Number of sales records to generate (default: 1,000,000)')
    
    parser.add_argument('--output', type=str, default='../data/sales_data.json', 
                        help='Output file path')
    
    parser.add_argument('--days', type=int, default=7, 
                        help='Number of days to spread the data over (default: 7)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Define time range (n days ago until now)
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=args.days)
    
    print(f"Generating {args.count:,} sales records from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}...")
    
    # Generate sales data
    sales_data = generate_sales_data(args.count, start_time, end_time)
    
    # Calculate size estimate
    record_sample = json.dumps(sales_data[0])
    approx_size_mb = (len(record_sample) * args.count) / (1024 * 1024)
    print(f"Estimated output size: {approx_size_mb:.2f} MB")
    
    # Write to file
    with open(args.output, 'w') as f:
        for record in sales_data:
            f.write(json.dumps(record) + '\n')
    
    # Get actual file size
    actual_size_mb = os.path.getsize(args.output) / (1024 * 1024)
    print(f"Generated {args.count:,} sales records")
    print(f"Actual file size: {actual_size_mb:.2f} MB")
    print(f"Data saved to {args.output}")

if __name__ == "__main__":
    main() 