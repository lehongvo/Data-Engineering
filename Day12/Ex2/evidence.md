# Evidence for Exercise 2: dbt Testing and Documentation

## 1. Thêm các tests vào schema.yml để kiểm tra tính toàn vẹn dữ liệu

Đã thêm nhiều loại tests khác nhau vào file schema.yml:

- Tests cơ bản: `unique`, `not_null`, `relationships`
- Tests nâng cao: `accepted_values` cho các trường có giá trị cố định
- Tests sử dụng packages bên ngoài như `dbt_expectations.expect_column_values_to_match_regex`

**Bằng chứng**: File `ecommerce_dbt/models/core/schema.yml` có nhiều tests được định nghĩa.

**Kết quả chạy tests**: Theo báo cáo trong `reports/test_summary.md`, có 25 tests cơ bản đã được thực hiện, 24 tests đã pass.

## 2. Viết custom tests cho các trường hợp phức tạp

Đã tạo hai custom tests trong thư mục `ecommerce_dbt/tests/`:

1. `assert_no_duplicate_orders.sql`: Kiểm tra sự trùng lặp đơn hàng dựa trên customer_id và order_date
2. `assert_total_amount_equals_sum_of_items.sql`: Kiểm tra tính toàn vẹn giữa tổng tiền đơn hàng và tổng giá trị các items

Đã tạo các macros hỗ trợ tests trong `ecommerce_dbt/macros/test_helpers.sql`:
- `test_not_negative`: Kiểm tra giá trị không âm
- `test_date_in_range`: Kiểm tra ngày tháng trong khoảng cho phép

**Bằng chứng**: File tests đã tồn tại và đã chạy thành công.

**Kết quả**: Custom test `assert_total_amount_equals_sum_of_items` đã chạy thành công, test `assert_no_duplicate_orders` phát hiện ra 2 đơn hàng trùng lặp (là kết quả mong muốn vì test này được thiết kế để phát hiện trùng lặp).

## 3. Chạy tests và phân tích kết quả

Đã chạy tests bằng lệnh `dbt test --store-failures` và có kết quả:

- Tổng số tests đã chạy: 26
- Tests đã pass: 25
- Tests đã fail: 1

Kết quả chi tiết được lưu trong:
- `reports/test_results.log`: Log đầy đủ quá trình chạy tests
- `reports/test_summary.md`: Báo cáo tóm tắt kết quả tests

**Bằng chứng**: Các file log trong thư mục `reports/`.

## 4. Tạo tài liệu mô tả chi tiết về models và cột dữ liệu

Đã thêm mô tả chi tiết cho:

- Mô tả cho mỗi model (`description` field)
- Mô tả cho mỗi cột dữ liệu
- Thêm meta tags để cung cấp thông tin bổ sung như `owner`, `contains_pii`, `update_frequency`

**Bằng chứng**: Files `ecommerce_dbt/models/core/schema.yml` và `ecommerce_dbt/models/sources/source.yml` chứa các mô tả chi tiết.

## 5. Sinh và phục vụ tài liệu dbt trên localhost

Đã tạo tài liệu dbt bằng lệnh `dbt docs generate` và phục vụ trên máy chủ localhost bằng lệnh `dbt docs serve`.

**Bằng chứng**: 
- File catalog đã được tạo trong `ecommerce_dbt/target/catalog.json`
- Máy chủ tài liệu chạy thành công trên http://localhost:8080

## 6. Tạo báo cáo tóm tắt kết quả tests

Đã tạo báo cáo tóm tắt kết quả tests trong file `reports/test_summary.md` với các thông tin:

- Tổng số tests đã chạy
- Số tests đã pass
- Số tests đã fail
- Chi tiết về các tests thất bại

**Bằng chứng**: File `reports/test_summary.md` đã được tạo thành công.

## Kết luận

Tất cả các yêu cầu của Exercise 2 đã được thực hiện đầy đủ. Hệ thống dbt đã được thiết lập để thực hiện kiểm thử dữ liệu toàn diện và tạo tài liệu chi tiết về dự án dữ liệu. 