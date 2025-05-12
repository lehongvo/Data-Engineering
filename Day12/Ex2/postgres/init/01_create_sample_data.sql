-- Tạo bảng khách hàng
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng sản phẩm
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng đơn hàng
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng chi tiết đơn hàng
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chèn dữ liệu mẫu cho khách hàng
INSERT INTO customers (name, email) VALUES
    ('Nguyễn Văn A', 'nguyenvana@example.com'),
    ('Trần Thị B', 'tranthib@example.com'),
    ('Lê Văn C', 'levanc@example.com');

-- Chèn dữ liệu mẫu cho sản phẩm
INSERT INTO products (name, price, category) VALUES
    ('Laptop Dell XPS', 25000000, 'Electronics'),
    ('iPhone 14', 20000000, 'Electronics'),
    ('Tai nghe Sony', 2000000, 'Electronics'),
    ('Áo thun', 200000, 'Clothing');

-- Chèn dữ liệu mẫu cho đơn hàng
INSERT INTO orders (customer_id, status) VALUES
    (1, 'completed'),
    (2, 'processing'),
    (1, 'completed');

-- Chèn dữ liệu mẫu cho chi tiết đơn hàng
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 25000000),
    (1, 3, 1, 2000000),
    (2, 2, 1, 20000000),
    (3, 4, 2, 200000); 