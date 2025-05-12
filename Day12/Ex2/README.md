# Bài tập 2: Kiểm thử và Tài liệu với dbt

## Tổng quan
Bài tập này tập trung vào việc thêm kiểm thử (tests) và tài liệu cho dự án dbt. Thông qua các kiểm thử tốt và tài liệu chi tiết, bạn có thể xây dựng lòng tin vào chất lượng dữ liệu và giúp người dùng hiểu rõ hơn về mô hình dữ liệu.

## Mục tiêu
1. Thêm các tests vào schema.yml để kiểm tra tính toàn vẹn dữ liệu
2. Viết custom tests cho các trường hợp phức tạp
3. Chạy tests và phân tích kết quả
4. Tạo tài liệu mô tả chi tiết về models và cột dữ liệu
5. Sinh và phục vụ tài liệu dbt trên localhost
6. Tạo báo cáo tóm tắt kết quả tests

## Cấu trúc thư mục
```
Ex2/
├── docker-compose.yml                      # Cấu hình Docker cho PostgreSQL
├── postgres/                               # Thư mục dữ liệu PostgreSQL
├── profiles.yml                            # Cấu hình kết nối dbt
├── ecommerce_dbt/                          # Dự án dbt
│   ├── dbt_project.yml                     # Cấu hình dự án dbt
│   ├── packages.yml                        # Danh sách packages cần cài đặt
│   ├── models/                             # Các mô hình dbt
│   │   ├── sources/                        # Định nghĩa nguồn dữ liệu
│   │   │   └── source.yml                  # Định nghĩa nguồn với tests
│   │   ├── staging/                        # Mô hình staging
│   │   │   ├── stg_customers.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_orders.sql
│   │   │   └── stg_order_items.sql
│   │   └── core/                           # Mô hình core
│   │       ├── dim_customers.sql
│   │       ├── dim_products.sql
│   │       ├── fct_orders.sql
│   │       └── schema.yml                  # Định nghĩa mô hình với tests
│   ├── tests/                              # Thư mục chứa custom tests
│   │   ├── assert_total_amount_equals_sum_of_items.sql
│   │   └── assert_no_duplicate_orders.sql
│   └── macros/                             # Macros hỗ trợ
│       ├── generate_schema_name.sql
│       └── test_helpers.sql
└── run.sh                                  # Script chạy dự án
```

## Các loại tests trong dbt

### 1. Generic tests (Tests chung)
Đây là các tests đơn giản, được định nghĩa trong file schema.yml và source.yml:
- **unique**: Kiểm tra các giá trị của cột là duy nhất
- **not_null**: Kiểm tra cột không chứa giá trị NULL
- **relationships**: Kiểm tra khóa ngoại
- **accepted_values**: Kiểm tra giá trị cột nằm trong tập hợp các giá trị cho phép

### 2. Custom generic tests (Tests chung tùy chỉnh)
- **test_not_negative**: Kiểm tra giá trị không âm
- **test_date_in_range**: Kiểm tra ngày trong khoảng cho phép
- **dbt_expectations.expect_column_values_to_match_regex**: Kiểm tra cột khớp với biểu thức regex
- **dbt_utils.expression_is_true**: Kiểm tra biểu thức là đúng

### 3. Singular tests (Tests riêng lẻ)
- **assert_total_amount_equals_sum_of_items.sql**: Kiểm tra tổng số tiền trong orders bằng tổng các mặt hàng
- **assert_no_duplicate_orders.sql**: Kiểm tra không có đơn hàng trùng lặp

## Tài liệu với dbt
dbt tự động tạo tài liệu dựa trên:
1. Cấu trúc dự án (models, sources, tests)
2. Mô tả trong schema.yml và source.yml
3. Metadata như tags và meta blocks

## Các bước thực hiện

### 1. Khởi động PostgreSQL và Thiết lập dbt
```bash
cd Ex2
./run.sh
```

### 2. Kiểm tra kết quả tests
Sau khi chạy script, một báo cáo tests sẽ được tạo trong thư mục `reports/`. Xem báo cáo để hiểu rõ hơn về các tests đã vượt qua và thất bại.

### 3. Xem tài liệu dbt
```bash
cd ecommerce_dbt
dbt docs serve
```
Mở trình duyệt và truy cập http://localhost:8080 để xem tài liệu.

## Tài liệu tham khảo
- [dbt Testing Documentation](https://docs.getdbt.com/docs/build/tests)
- [dbt Documentation Documentation](https://docs.getdbt.com/docs/collaborate/documentation)
- [dbt Utils Package](https://github.com/dbt-labs/dbt-utils)
- [dbt Expectations Package](https://github.com/calogica/dbt-expectations) 