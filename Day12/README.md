# Ngày 12: Phát triển Data Engineering với dbt

## dbt là gì?
dbt (data build tool) là một công cụ chuyển đổi dữ liệu cho phép các nhà phân tích dữ liệu và kỹ sư dữ liệu chuyển đổi dữ liệu trong kho dữ liệu bằng cách viết SQL đơn giản. dbt xử lý công việc ELT (Extract, Load, Transform) một cách hiệu quả và dễ dàng.

### Lợi ích của dbt:
- **Tập trung vào SQL**: Chỉ cần biết SQL bạn đã có thể sử dụng dbt
- **Modularity**: Chia mô hình dữ liệu thành các thành phần nhỏ, dễ quản lý
- **Kiểm thử dữ liệu**: Tích hợp kiểm thử để đảm bảo chất lượng dữ liệu
- **Tài liệu hóa**: Tự động tạo tài liệu cho mô hình dữ liệu
- **Quản lý phiên bản**: Làm việc với Git để theo dõi thay đổi
- **Tái sử dụng mã**: Sử dụng macro, package để tái sử dụng mã

## Kiến trúc dbt
dbt hoạt động như một lớp chuyển đổi trong pipeline dữ liệu:

1. **Sources**: Dữ liệu thô từ nguồn (database, data warehouse)
2. **Staging**: Mô hình đầu tiên, làm sạch và chuẩn hóa dữ liệu
3. **Intermediate**: Các bảng trung gian kết hợp nhiều nguồn
4. **Marts**: Mô hình cuối cùng được tối ưu hóa cho việc phân tích

## Yêu cầu chuẩn bị
- Docker và Docker Compose đã cài đặt
- Kiến thức cơ bản về SQL
- Hiểu biết cơ bản về PostgreSQL
- Tài khoản Git/GitHub

## Bài tập thực hành

### Bài tập 1: Thiết lập mô hình dbt với PostgreSQL
Trong bài tập này, bạn sẽ:
1. Thiết lập database PostgreSQL và tạo dữ liệu mẫu
2. Cài đặt dbt
3. Khởi tạo dự án dbt
4. Tạo các mô hình staging và core
5. Chạy và kiểm tra mô hình của bạn

#### Bước 1: Thiết lập PostgreSQL với Docker
```bash
# Tạo thư mục cho dữ liệu PostgreSQL
mkdir -p postgres/data postgres/init

# Tạo file docker-compose.yml
cat > docker-compose.yml << EOL
version: '3'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: dbt_user
      POSTGRES_PASSWORD: dbt_password
      POSTGRES_DB: dbt_db
    ports:
      - "5432:5432"
    volumes:
      - ./postgres/data:/var/lib/postgresql/data
      - ./postgres/init:/docker-entrypoint-initdb.d
EOL

# Tạo script khởi tạo dữ liệu mẫu
cat > postgres/init/01_create_sample_data.sql << EOL
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
EOL

# Khởi động PostgreSQL
docker-compose up -d
```

#### Bước 2: Cài đặt dbt
```bash
# Cài đặt dbt với PostgreSQL adapter
pip install dbt-postgres
```

#### Bước 3: Khởi tạo dự án dbt
```bash
# Khởi tạo dự án dbt
dbt init ecommerce_dbt
cd ecommerce_dbt
```

#### Bước 4: Cấu hình kết nối
Tạo file `~/.dbt/profiles.yml` với nội dung:
```yaml
ecommerce_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: dbt_user
      password: dbt_password
      port: 5432
      dbname: dbt_db
      schema: public
      threads: 4
```

#### Bước 5: Tạo các mô hình dbt
Tạo file `models/staging/stg_customers.sql`:
```sql
with source as (
    select * from {{ source('ecommerce_raw', 'customers') }}
),

staged as (
    select
        customer_id,
        name,
        email,
        created_at
    from source
)

select * from staged
```

Tạo file `models/core/dim_customers.sql`:
```sql
with customers as (
    select * from {{ ref('stg_customers') }}
)

select
    customer_id,
    name,
    email,
    created_at,
    current_timestamp as updated_at
from customers
```

#### Bước 6: Chạy và kiểm tra mô hình
```bash
# Chạy mô hình
dbt run

# Kiểm tra mô hình
dbt test
```

### Bài tập 2: Thêm kiểm thử và tài liệu
Trong bài tập này, bạn sẽ:
1. Thêm các kiểm thử cho mô hình dữ liệu
2. Tạo tài liệu cho mô hình dữ liệu
3. Xem tài liệu

#### Bước 1: Thêm kiểm thử
Tạo file `models/schema.yml`:
```yaml
version: 2

models:
  - name: dim_customers
    description: Bảng khách hàng đã được xử lý
    columns:
      - name: customer_id
        description: Khóa chính của bảng khách hàng
        tests:
          - unique
          - not_null
      - name: email
        description: Địa chỉ email của khách hàng
        tests:
          - unique
```

#### Bước 2: Tạo tài liệu
```bash
# Tạo tài liệu
dbt docs generate

# Khởi động máy chủ xem tài liệu
dbt docs serve
```

#### Bước 3: Xem tài liệu
Mở trình duyệt và truy cập địa chỉ: http://localhost:8080

## Tài liệu tham khảo
- [Tài liệu chính thức dbt](https://docs.getdbt.com/)
- [Các thực hành tốt nhất với dbt](https://docs.getdbt.com/guides/best-practices)
- [Cộng đồng dbt](https://discourse.getdbt.com/)
