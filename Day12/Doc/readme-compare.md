# Giải thích dbt qua ví dụ

**dbt (data build tool)** là một framework mã nguồn mở dùng để chuyển đổi dữ liệu trong kho lưu trữ dữ liệu. Để hiểu rõ hơn, hãy xem qua một ví dụ cụ thể:

## Tình huống thực tế

Giả sử bạn đang làm việc với dữ liệu bán hàng cho một cửa hàng trực tuyến. Bạn có các bảng dữ liệu thô như sau:

1. `raw_orders` - Thông tin đơn hàng
2. `raw_customers` - Thông tin khách hàng
3. `raw_products` - Thông tin sản phẩm
4. `raw_order_items` - Chi tiết sản phẩm trong mỗi đơn hàng

## Không có dbt (Cách truyền thống)

Trước đây, quá trình phân tích có thể như sau:

1. Viết các SQL query thủ công để chuyển đổi dữ liệu
2. Lưu các query dưới dạng file hoặc script riêng lẻ
3. Chạy các query theo một thứ tự nhất định
4. Quản lý thủ công khi có sự thay đổi

Ví dụ query:

```sql
-- Script 1: customers_cleaned.sql
CREATE OR REPLACE VIEW customers_cleaned AS
SELECT
  customer_id,
  first_name,
  last_name,
  email,
  CASE
    WHEN state IN ('CA', 'ca', 'California') THEN 'California'
    WHEN state IN ('NY', 'ny', 'New York') THEN 'New York'
    ELSE state
  END AS state,
  created_at
FROM raw_customers
WHERE deleted_at IS NULL;

-- Script 2: order_items_cleaned.sql
CREATE OR REPLACE VIEW order_items_cleaned AS
SELECT
  order_id,
  product_id,
  quantity,
  price,
  quantity * price AS total_amount
FROM raw_order_items;

-- Script 3: customer_orders.sql
CREATE OR REPLACE VIEW customer_orders AS
SELECT
  c.customer_id,
  c.first_name,
  c.last_name,
  COUNT(DISTINCT o.order_id) AS order_count,
  SUM(oi.total_amount) AS lifetime_value
FROM customers_cleaned c
JOIN raw_orders o ON c.customer_id = o.customer_id
JOIN order_items_cleaned oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name;
```

**Vấn đề**:
- Không rõ thứ tự chạy
- Không quản lý phụ thuộc
- Khó tái sử dụng code
- Không có tests
- Không có tài liệu tự động

## Với dbt (Cách tiếp cận hiện đại)

### 1. Cấu trúc dự án dbt

```
retail_analytics/
├── dbt_project.yml            # Cấu hình dự án
├── models/
│   ├── schema.yml             # Lược đồ và tests
│   ├── staging/               # Mô hình dữ liệu stage đầu tiên
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   ├── stg_products.sql
│   │   └── stg_order_items.sql
│   ├── intermediate/          
│   │   └── int_order_items_with_cost.sql
│   └── marts/                 # Mô hình dữ liệu cho phân tích
│       ├── core/
│       │   ├── dim_customers.sql
│       │   ├── dim_products.sql 
│       │   ├── fct_orders.sql
│       │   └── fct_order_items.sql
│       └── marketing/
│           └── customer_lifetime_value.sql
├── tests/
│   └── ensure_customer_ltv_makes_sense.sql
└── macros/
    └── clean_state_names.sql
```

### 2. Định nghĩa sources (nguồn dữ liệu)

```yaml
# models/schema.yml
version: 2

sources:
  - name: raw
    database: retail_db  # Tên database trong PostgreSQL
    schema: public       # Schema chứa bảng dữ liệu
    tables:
      - name: raw_customers
      - name: raw_orders
      - name: raw_products
      - name: raw_order_items
```

### 3. Models dbt (SQL với template)

```sql
-- models/staging/stg_customers.sql
SELECT
  customer_id,
  first_name,
  last_name,
  email,
  {{ clean_state_names('state') }} AS state,
  created_at
FROM {{ source('raw', 'raw_customers') }}
WHERE deleted_at IS NULL
```

```sql
-- models/staging/stg_order_items.sql
SELECT
  order_id,
  product_id,
  quantity,
  price,
  quantity * price AS total_amount
FROM {{ source('raw', 'raw_order_items') }}
```

```sql
-- models/marts/marketing/customer_lifetime_value.sql
SELECT
  c.customer_id,
  c.first_name,
  c.last_name,
  COUNT(DISTINCT o.order_id) AS order_count,
  SUM(oi.total_amount) AS lifetime_value
FROM {{ ref('dim_customers') }} c
JOIN {{ ref('fct_orders') }} o ON c.customer_id = o.customer_id
JOIN {{ ref('fct_order_items') }} oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
```

### 4. Định nghĩa macros (như hàm tùy chỉnh)

```sql
-- macros/clean_state_names.sql
{% macro clean_state_names(column_name) %}
  CASE
    WHEN {{ column_name }} IN ('CA', 'ca', 'California') THEN 'California'
    WHEN {{ column_name }} IN ('NY', 'ny', 'New York') THEN 'New York'
    ELSE {{ column_name }}
  END
{% endmacro %}
```

### 5. Thêm tests vào schema

```yaml
# models/schema.yml
models:
  - name: dim_customers
    description: "Thông tin chi tiết về khách hàng"
    columns:
      - name: customer_id
        description: "ID duy nhất của khách hàng"
        tests:
          - unique
          - not_null
      - name: email
        description: "Email của khách hàng"
        tests:
          - unique
          - not_null

  - name: customer_lifetime_value
    description: "Phân tích giá trị khách hàng theo thời gian"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: lifetime_value
        description: "Tổng giá trị đơn hàng của khách hàng"
        tests:
          - not_null
          - positive_value  # Custom test
```

### 6. Chạy dbt

```bash
# Chạy tất cả models
dbt run

# Chạy models cụ thể
dbt run --models customer_lifetime_value

# Chạy tests
dbt test

# Tạo tài liệu
dbt docs generate
dbt docs serve
```

### 7. Kết quả của dbt docs

Khi chạy `dbt docs serve`, bạn sẽ nhận được một trang web tài liệu tự động với:
- Sơ đồ phụ thuộc giữa các models
- Mô tả của từng model và cột
- Kết quả test
- Lineage graph (đồ thị phả hệ) hiển thị dữ liệu đi từ nguồn đến đích

## Lợi ích của dbt trong ví dụ này

1. **Modularity (Tính mô-đun)**: Mỗi model SQL được tách riêng và có thể tái sử dụng
2. **Dependencies (Phụ thuộc tự động)**: Hàm `ref()` xác định phụ thuộc giữa các model
3. **DRY (Don't Repeat Yourself)**: Dùng macros cho code lặp lại
4. **Testing (Kiểm thử)**: Đảm bảo chất lượng dữ liệu
5. **Documentation (Tài liệu)**: Tự động tạo tài liệu cho dự án
6. **Versioning (Kiểm soát phiên bản)**: Dễ dàng làm việc với Git
7. **Environment (Môi trường)**: Phân tách dev/prod

Ví dụ này cho thấy dbt không thay thế SQL mà **làm phong phú thêm** SQL bằng cách thêm các khái niệm kỹ thuật phần mềm hiện đại để việc quản lý chuyển đổi dữ liệu trở nên bền vững và dễ bảo trì hơn.