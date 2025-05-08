import time
import random
import json
from datetime import datetime
from kafka import KafkaProducer

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Topic for e-commerce transactions
topic = 'ecommerce-transactions'

# Product data for simulation
PRODUCTS = [
    {"id": 101, "name": "Smartphone", "price": 699.99},
    {"id": 102, "name": "Laptop", "price": 1299.99},
    {"id": 103, "name": "Headphones", "price": 149.99},
    {"id": 104, "name": "Tablet", "price": 349.99},
    {"id": 105, "name": "Smartwatch", "price": 199.99},
    {"id": 106, "name": "Camera", "price": 599.99},
    {"id": 107, "name": "Gaming Console", "price": 499.99},
    {"id": 108, "name": "Bluetooth Speaker", "price": 79.99},
    {"id": 109, "name": "External Hard Drive", "price": 129.99},
    {"id": 110, "name": "Wireless Earbuds", "price": 119.99}
]

# Total number of simulated users
NUM_USERS = 100

print("E-commerce Transaction Producer started. Sending transaction data...")

try:
    while True:
        # Generate a random user ID (some users will be more active)
        user_weight = random.random()
        if user_weight < 0.2:  # 20% of transactions from high-value customers (IDs 1-10)
            user_id = random.randint(1, 10)
        else:  # 80% of transactions from regular customers
            user_id = random.randint(11, NUM_USERS)
        
        # Select a random product
        product = random.choice(PRODUCTS)
        product_id = product["id"]
        
        # Generate a random quantity (high-value customers tend to buy more)
        quantity = 1
        if user_id <= 10:  # High-value customers
            quantity = random.randint(1, 5)
        else:
            quantity = random.randint(1, 2)
        
        # Calculate total amount
        base_price = product["price"]
        amount = round(base_price * quantity, 2)
        
        # Create transaction
        transaction = {
            "transaction_id": random.randint(10000, 99999),
            "user_id": user_id,
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": quantity,
            "amount": amount,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Send to Kafka
        producer.send(topic, transaction)
        
        # Print sent transaction
        print(f"Sent: {transaction}")
        
        # Random delay between transactions (0.5 to 2 seconds)
        time.sleep(random.uniform(0.5, 2))
        
except KeyboardInterrupt:
    print("Transaction Producer stopped.")
finally:
    producer.close() 