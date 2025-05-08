CREATE TABLE IF NOT EXISTS sales (
  product_id INT NOT NULL,
  store_id INT NOT NULL,
  date TEXT NOT NULL,
  quantity INT NOT NULL,
  revenue DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  product_id INT PRIMARY KEY,
  product_name TEXT NOT NULL,
  category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stores (
  store_id INT PRIMARY KEY,
  store_name TEXT NOT NULL,
  region TEXT NOT NULL
);

-- Insert sample data
INSERT INTO products VALUES 
  (1, 'Laptop', 'Electronics'),
  (2, 'Smartphone', 'Electronics'),
  (3, 'T-shirt', 'Clothing');

INSERT INTO stores VALUES
  (1, 'Main Store', 'North'),
  (2, 'Mall Shop', 'South'),
  (3, 'Online Store', 'Online');

INSERT INTO sales VALUES
  (1, 1, '2023-01-01', 5, 100.0),
  (2, 1, '2023-01-01', 3, 150.0),
  (3, 2, '2023-01-02', 2, 50.0),
  (1, 2, '2023-01-02', 10, 200.0),
  (2, 3, '2023-01-03', 7, 350.0); 