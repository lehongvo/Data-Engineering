-- Enable logical replication for Debezium
ALTER SYSTEM SET wal_level = logical;

-- Create tables for e-commerce data
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    inventory INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO customers (name, email) VALUES
    ('John Doe', 'john.doe@example.com'),
    ('Jane Smith', 'jane.smith@example.com'),
    ('Bob Johnson', 'bob.johnson@example.com'),
    ('Alice Brown', 'alice.brown@example.com'),
    ('Charlie Davis', 'charlie.davis@example.com');

INSERT INTO products (name, description, price, inventory) VALUES
    ('Smartphone', 'Latest smartphone with advanced features', 799.99, 50),
    ('Laptop', 'High-performance laptop for professionals', 1299.99, 30),
    ('Wireless Headphones', 'Noise-cancelling wireless headphones', 199.99, 100),
    ('Smart Watch', 'Fitness and health tracking smartwatch', 249.99, 75),
    ('Tablet', 'Lightweight tablet with long battery life', 349.99, 45),
    ('Bluetooth Speaker', 'Portable bluetooth speaker with great sound', 79.99, 120),
    ('Gaming Console', 'Next-generation gaming console', 499.99, 25),
    ('Digital Camera', 'Professional digital camera', 699.99, 15);

INSERT INTO orders (customer_id, total_amount, status) VALUES
    (1, 1099.98, 'completed'),
    (2, 349.99, 'processing'),
    (3, 699.99, 'completed'),
    (4, 279.98, 'completed'),
    (5, 1799.98, 'processing'),
    (1, 499.99, 'pending');

-- Create a publication for CDC
CREATE PUBLICATION dbz_publication FOR TABLE customers, products, orders; 