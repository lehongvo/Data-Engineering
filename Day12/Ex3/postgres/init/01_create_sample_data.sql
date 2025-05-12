-- Create sample tables for e-commerce system

-- Customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    inventory_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    payment_method VARCHAR(50),
    shipping_address TEXT,
    shipping_cost DECIMAL(12,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample customers
INSERT INTO customers (name, email, phone) VALUES
('John Doe', 'john.doe@example.com', '123-456-7890'),
('Jane Smith', 'jane.smith@example.com', '123-456-7891'),
('Robert Johnson', 'robert.johnson@example.com', '123-456-7892'),
('Emily Davis', 'emily.davis@example.com', '123-456-7893'),
('Michael Brown', 'michael.brown@example.com', '123-456-7894'),
('Sarah Wilson', 'sarah.wilson@example.com', '123-456-7895'),
('David Taylor', 'david.taylor@example.com', '123-456-7896'),
('Jennifer Lee', 'jennifer.lee@example.com', '123-456-7897'),
('Richard Moore', 'richard.moore@example.com', '123-456-7898'),
('Patricia White', 'patricia.white@example.com', '123-456-7899');

-- Insert sample products
INSERT INTO products (name, price, category, inventory_count, is_active) VALUES
('Smartphone X', 12000000, 'Electronics', 100, TRUE),
('Laptop Pro', 20000000, 'Electronics', 50, TRUE),
('Wireless Headphones', 2000000, 'Electronics', 200, TRUE),
('T-shirt Basic', 200000, 'Clothing', 500, TRUE),
('Jeans Regular', 500000, 'Clothing', 300, TRUE),
('Hoodie Casual', 350000, 'Clothing', 200, TRUE),
('Running Shoes', 800000, 'Footwear', 150, TRUE),
('Casual Sneakers', 600000, 'Footwear', 200, TRUE),
('Leather Wallet', 300000, 'Accessories', 250, TRUE),
('Watch Classic', 1500000, 'Accessories', 100, TRUE),
('Smartwatch', 3000000, 'Electronics', 80, TRUE),
('Tablet Mini', 5000000, 'Electronics', 60, TRUE),
('Winter Jacket', 1200000, 'Clothing', 100, TRUE),
('Formal Shoes', 900000, 'Footwear', 80, TRUE),
('Backpack', 450000, 'Accessories', 150, TRUE);

-- Insert sample orders
-- For realistic data, we'll create orders with different dates spanning the last few months
DO $$
DECLARE
    random_customer_id INTEGER;
    random_order_date TIMESTAMP;
    random_status VARCHAR;
    random_payment VARCHAR;
    random_shipping_cost DECIMAL;
    random_total DECIMAL;
    new_order_id INTEGER;
    statuses VARCHAR[] := ARRAY['completed', 'processing', 'cancelled', 'refunded'];
    payment_methods VARCHAR[] := ARRAY['credit_card', 'debit_card', 'e-wallet', 'bank_transfer'];
    i INTEGER;
BEGIN
    FOR i IN 1..100 LOOP
        -- Generate random values
        random_customer_id := floor(random() * 10) + 1;
        random_order_date := NOW() - (random() * INTERVAL '180 days');
        random_status := statuses[floor(random() * 4) + 1];
        random_payment := payment_methods[floor(random() * 4) + 1];
        random_shipping_cost := (floor(random() * 10) + 1) * 10000;
        random_total := 0; -- Will be calculated after adding items
        
        -- Insert order (total will be updated later)
        INSERT INTO orders (customer_id, order_date, status, payment_method, shipping_address, shipping_cost, total_amount)
        VALUES (
            random_customer_id,
            random_order_date,
            random_status,
            random_payment,
            'Sample Address ' || i,
            random_shipping_cost,
            0
        ) RETURNING order_id INTO new_order_id;
        
        -- Add 1-5 items to each order
        DECLARE
            j INTEGER;
            items_count INTEGER := floor(random() * 5) + 1;
            random_product_id INTEGER;
            random_quantity INTEGER;
            random_unit_price DECIMAL;
            random_discount DECIMAL;
            item_total DECIMAL;
            order_total DECIMAL := 0;
        BEGIN
            FOR j IN 1..items_count LOOP
                random_product_id := floor(random() * 15) + 1;
                random_quantity := floor(random() * 3) + 1;
                
                -- Get actual product price
                SELECT price INTO random_unit_price 
                FROM products 
                WHERE product_id = random_product_id;
                
                -- Calculate random discount (0-10% of unit price)
                random_discount := floor(random() * 11) * (random_unit_price * 0.01);
                
                -- Calculate item total
                item_total := (random_unit_price * random_quantity) - random_discount;
                order_total := order_total + item_total;
                
                -- Insert order item
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount_amount)
                VALUES (
                    new_order_id,
                    random_product_id,
                    random_quantity,
                    random_unit_price,
                    random_discount
                );
            END LOOP;
            
            -- Update order total
            UPDATE orders 
            SET total_amount = order_total + random_shipping_cost
            WHERE order_id = new_order_id;
        END;
    END LOOP;
END $$; 