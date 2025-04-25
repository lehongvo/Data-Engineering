# Data Engineering Infrastructure với GCP

Project này tạo data infrastructure trên Google Cloud Platform (GCP) với các thành phần:
- VPC Network và Subnet
- Cloud Storage Bucket cho data lake
- BigQuery Dataset và Table cho data warehouse

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

2. Xem trước thay đổi (thay YOUR_PROJECT_ID bằng ID project của bạn):
   ```bash
   terraform plan -var="project_id=YOUR_PROJECT_ID"
   ```

3. Tạo infrastructure:
   ```bash
   terraform apply -var="project_id=YOUR_PROJECT_ID"
   ```

4. Xóa infrastructure:
   ```bash
   terraform destroy -var="project_id=YOUR_PROJECT_ID"
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