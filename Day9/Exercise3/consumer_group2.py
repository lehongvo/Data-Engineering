import json
from kafka import KafkaConsumer
from collections import defaultdict
from datetime import datetime

# Initialize Kafka consumer with the second consumer group
consumer = KafkaConsumer(
    'ecommerce-transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='user-behavior-analyzer',
    enable_auto_commit=True
)

print("Consumer Group 2 started: Analyzing user behavior and identifying high-value customers")
print("===================================================================================")

# Dictionary to store user metrics
user_spending = defaultdict(float)        # Total spending by user
user_transaction_count = defaultdict(int) # Number of transactions by user
user_products = defaultdict(set)          # Unique products purchased by user
user_last_activity = defaultdict(str)     # Last activity timestamp

# For periodic reporting
transaction_count = 0
REPORTING_THRESHOLD = 10  # Report after every 10 transactions
HIGH_VALUE_THRESHOLD = 1000.00  # Users with spending above this are high-value

try:
    for message in consumer:
        # Extract transaction data
        transaction = message.value
        user_id = transaction["user_id"]
        amount = transaction["amount"]
        product_id = transaction["product_id"]
        timestamp = transaction["timestamp"]
        
        # Update user metrics
        user_spending[user_id] += amount
        user_transaction_count[user_id] += 1
        user_products[user_id].add(product_id)
        user_last_activity[user_id] = timestamp
        
        # Increment transaction counter
        transaction_count += 1
        
        # Print individual transaction
        print(f"Processed: User {user_id} purchased ${amount:.2f}")
        
        # Periodically show user behavior analysis
        if transaction_count % REPORTING_THRESHOLD == 0:
            print("\n===== USER BEHAVIOR ANALYSIS =====")
            
            # Identify high-value customers (sort by spending)
            sorted_users = sorted(
                user_spending.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            # Print top 5 users by spending
            print("Top 5 customers by spending:")
            for i, (uid, spending) in enumerate(sorted_users[:5], 1):
                product_diversity = len(user_products[uid])
                avg_order_value = spending / user_transaction_count[uid]
                
                status = "HIGH-VALUE" if spending > HIGH_VALUE_THRESHOLD else "Regular"
                
                print(f"{i}. User {uid} ({status})")
                print(f"   Total Spending: ${spending:.2f}")
                print(f"   Transactions: {user_transaction_count[uid]}")
                print(f"   Avg Order Value: ${avg_order_value:.2f}")
                print(f"   Product Diversity: {product_diversity} unique products")
                print(f"   Last Active: {user_last_activity[uid]}")
            
            # Count of high-value customers
            high_value_count = sum(1 for spending in user_spending.values() if spending > HIGH_VALUE_THRESHOLD)
            total_users = len(user_spending)
            print(f"\nHigh-value customers: {high_value_count} out of {total_users} ({high_value_count/total_users*100:.1f}%)")
            
            print("===================================\n")

except KeyboardInterrupt:
    print("Consumer Group 2 stopped.")
finally:
    consumer.close() 