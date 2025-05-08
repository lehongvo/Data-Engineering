import json
from kafka import KafkaConsumer
from collections import defaultdict

# Initialize Kafka consumer with the first consumer group
consumer = KafkaConsumer(
    'ecommerce-transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='revenue-aggregator',
    enable_auto_commit=True
)

print("Consumer Group 1 started: Aggregating revenue by product")
print("======================================================")

# Dictionary to store product revenue
product_revenue = defaultdict(float)
product_count = defaultdict(int)
product_names = {}

# For periodic reporting
transaction_count = 0
REPORTING_THRESHOLD = 10  # Report after every 10 transactions

try:
    for message in consumer:
        # Extract transaction data
        transaction = message.value
        product_id = transaction["product_id"]
        product_name = transaction["product_name"]
        amount = transaction["amount"]
        
        # Update revenue for this product
        product_revenue[product_id] += amount
        product_count[product_id] += transaction["quantity"]
        product_names[product_id] = product_name
        
        # Increment transaction counter
        transaction_count += 1
        
        # Print individual transaction
        print(f"Processed: {transaction['product_name']} - ${amount:.2f}")
        
        # Periodically show aggregated data
        if transaction_count % REPORTING_THRESHOLD == 0:
            print("\n===== PRODUCT REVENUE SUMMARY =====")
            
            # Sort products by revenue (highest first)
            sorted_products = sorted(
                product_revenue.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            # Print revenue for each product
            for prod_id, revenue in sorted_products:
                print(f"{product_names[prod_id]}: ${revenue:.2f} (Sold: {product_count[prod_id]} units)")
            
            print(f"Total Revenue: ${sum(product_revenue.values()):.2f}")
            print("===================================\n")

except KeyboardInterrupt:
    print("Consumer Group 1 stopped.")
finally:
    consumer.close() 