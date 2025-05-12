# Bài tập 1: Thiết lập mô hình dbt với PostgreSQL

## Mô tả
Bài tập này cung cấp một dự án mẫu sử dụng dbt (data build tool) để chuyển đổi dữ liệu từ một cơ sở dữ liệu PostgreSQL. Dự án bao gồm các mô hình staging và core để xử lý dữ liệu e-commerce đơn giản.

## Cấu trúc thư mục
```
Ex1/
├── docker-compose.yml                      # Cấu hình Docker cho PostgreSQL
├── postgres/
│   ├── data/                               # Thư mục lưu dữ liệu PostgreSQL
│   └── init/
│       └── 01_create_sample_data.sql       # Script khởi tạo dữ liệu mẫu
├── ecommerce_dbt/                          # Dự án dbt
│   ├── dbt_project.yml                     # Cấu hình dự án dbt
│   └── models/                             # Các mô hình dbt
│       ├── sources/                        # Định nghĩa nguồn dữ liệu
│       │   └── source.yml
│       ├── staging/                        # Mô hình staging
│       │   ├── stg_customers.sql
│       │   ├── stg_products.sql
│       │   ├── stg_orders.sql
│       │   └── stg_order_items.sql
│       └── core/                           # Mô hình core
│           ├── dim_customers.sql
│           ├── dim_products.sql
│           └── fact_orders.sql
└── profiles.yml                            # Cấu hình kết nối dbt
```

## Các bước thực hiện

### 1. Khởi động PostgreSQL với Docker
```bash
cd Ex1
docker-compose up -d
```

### 2. Cài đặt dbt
```bash
pip install dbt-postgres
```

### 3. Cấu hình dbt profile
Sao chép file `profiles.yml` vào thư mục `~/.dbt/` hoặc tạo biến môi trường:
```bash
mkdir -p ~/.dbt
cp profiles.yml ~/.dbt/
```

### 4. Chạy các mô hình dbt
```bash
cd ecommerce_dbt
dbt run
```

### 5. Kiểm tra mô hình
```bash
dbt test
```

### 6. Tạo tài liệu
```bash
dbt docs generate
dbt docs serve
```

## Kết quả
Sau khi chạy các lệnh trên, bạn sẽ có:
1. Bảng staging (view): chứa dữ liệu được làm sạch từ nguồn
2. Bảng dimension (table): chứa thông tin về khách hàng và sản phẩm
3. Bảng fact (table): chứa thông tin về đơn hàng cùng với tổng số tiền và số lượng mặt hàng

## Lưu ý
- Đảm bảo Docker đang chạy trước khi bắt đầu
- Đảm bảo cổng 5432 không bị sử dụng bởi dịch vụ khác
- Nếu bạn muốn kết nối trực tiếp đến PostgreSQL:
  ```bash
  psql -h localhost -U dbt_user -d dbt_db
  # Mật khẩu: dbt_password
  ``` 