# Data Engineering Infrastructure với GCP

## Giới thiệu về Terraform

Terraform là một công cụ Infrastructure as Code (IaC) mã nguồn mở, cho phép bạn xây dựng, thay đổi và quản lý infrastructure một cách an toàn và hiệu quả. Terraform sử dụng cú pháp khai báo đơn giản để mô tả infrastructure và quản lý vòng đời của nó.

Project này tạo data infrastructure trên Google Cloud Platform (GCP) với các thành phần:
- VPC Network và Subnet
- Cloud Storage Bucket cho data lake
- BigQuery Dataset và Table cho data warehouse

## Các khái niệm chính

### VPC (Virtual Private Cloud)
VPC là một mạng ảo được tạo ra trong môi trường cloud, cô lập và an toàn, cho phép bạn triển khai các tài nguyên cloud trong một mạng ảo được xác định. VPC giúp:
- **Cô lập**: Tách biệt tài nguyên của bạn với người dùng khác trên cloud
- **Kiểm soát kết nối**: Quyết định những gì có thể kết nối vào và ra khỏi môi trường của bạn
- **Khả năng mở rộng**: Dễ dàng mở rộng quy mô theo nhu cầu
- **Kết nối lai**: Kết nối an toàn giữa môi trường cloud và on-premise

Trong VPC, **Subnet** là các phân đoạn mạng nhỏ hơn giúp tổ chức và quản lý tài nguyên trong các khu vực khác nhau và tăng cường bảo mật bằng cách cô lập các nhóm tài nguyên.

## Cấu trúc file Terraform

Project này bao gồm các file chính:
- `main.tf`: Chứa các resource và cấu hình chính
- `variables.tf`: Định nghĩa các biến sử dụng trong project
- `outputs.tf`: Định nghĩa các giá trị đầu ra sau khi apply

## Yêu cầu trước khi bắt đầu

1. Cài đặt Terraform:
   ```bash
   brew install terraform
   ```

2. Cài đặt và cấu hình Google Cloud SDK:
   ```bash
   brew install google-cloud-sdk
   gcloud init
   ```

3. Tạo Service Account và download key JSON:
   - Truy cập Google Cloud Console
   - Vào IAM & Admin > Service Accounts
   - Tạo service account mới với quyền:
     - Compute Network Admin
     - Storage Admin
     - BigQuery Admin
   - Tạo và download key JSON

4. Set environment variable cho credentials:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

## Các bước thực hiện

1. Khởi tạo project:
   ```bash
   terraform init
   ```
   *Giải thích*: Lệnh này tải các provider và module cần thiết được chỉ định trong file cấu hình Terraform của bạn. Nó cũng thiết lập backend để lưu trữ trạng thái.

2. Xem trước thay đổi (thay YOUR_PROJECT_ID bằng ID project của bạn):
   ```bash
   terraform plan -var="project_id=YOUR_PROJECT_ID"
   ```
   *Giải thích*: Lệnh này tạo một kế hoạch thực thi, hiển thị những thay đổi Terraform sẽ thực hiện mà không làm thay đổi thực tế infrastructure.

3. Tạo infrastructure:
   ```bash
   terraform apply -var="project_id=YOUR_PROJECT_ID"
   ```
   *Giải thích*: Lệnh này triển khai thay đổi vào infrastructure thực tế. Bạn sẽ được yêu cầu xác nhận bằng cách gõ "yes" trước khi các thay đổi được áp dụng.

4. Xóa infrastructure:
   ```bash
   terraform destroy -var="project_id=YOUR_PROJECT_ID"
   ```
   *Giải thích*: Lệnh này xóa tất cả các resource đã được tạo. Cẩn thận khi sử dụng lệnh này trong môi trường production.

## Kiểm tra infrastructure sau khi triển khai

Sau khi triển khai thành công, bạn có thể kiểm tra:

1. Xác nhận VPC và subnet:
   ```bash
   gcloud compute networks list --project=YOUR_PROJECT_ID
   gcloud compute networks subnets list --project=YOUR_PROJECT_ID
   ```

2. Xác nhận Cloud Storage bucket:
   ```bash
   gcloud storage ls --project=YOUR_PROJECT_ID
   ```

3. Xác nhận BigQuery dataset và table:
   ```bash
   bq ls --project_id=YOUR_PROJECT_ID
   bq show --project_id=YOUR_PROJECT_ID DATASET_NAME.TABLE_NAME
   ```

## Cấu trúc Data Lake

- Raw data được lưu trong Cloud Storage với cấu trúc:
  ```
  gs://{project-name}-data-lake-{environment}/raw/sales/YYYY/MM/DD/
  ```

- Data được tự động chuyển sang storage class NEARLINE sau 30 ngày

## BigQuery Integration

- Dataset được tạo với tên: {project_name}_{environment}
- Table raw_sales_data được partition theo ngày (transaction_date)
- Schema bao gồm:
  - transaction_id (STRING)
  - customer_id (STRING)
  - amount (FLOAT)
  - transaction_date (TIMESTAMP)

## Biến môi trường

- `project_id`: ID của GCP Project (required)
- `region`: GCP Region (default: "asia-southeast1")
- `environment`: Môi trường deployment (default: "dev")
- `project_name`: Tên project (default: "data-engineering-practice")
- `subnet_cidr`: CIDR block cho subnet (default: "10.0.0.0/24")

## Mẹo xử lý lỗi thường gặp

1. **Lỗi xác thực**: Nếu gặp lỗi xác thực, hãy kiểm tra:
   - Service account có đủ quyền
   - GOOGLE_APPLICATION_CREDENTIALS đã được set đúng
   - Key JSON không bị hỏng

2. **Lỗi resource đã tồn tại**: Nếu resource đã tồn tại:
   - Thử import resource vào state: `terraform import [address] [ID]`
   - Hoặc xóa resource thủ công và chạy lại terraform

3. **Lỗi provider**: Nếu gặp lỗi liên quan đến provider:
   - Xóa thư mục .terraform và chạy lại `terraform init`
   - Kiểm tra phiên bản provider tương thích

## Tài liệu tham khảo

- [Terraform Documentation](https://www.terraform.io/docs)
- [Google Cloud Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Terraform Best Practices](https://cloud.google.com/docs/terraform/best-practices-for-terraform)
- [Learn Terraform](https://learn.hashicorp.com/terraform)