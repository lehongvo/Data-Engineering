# Data Engineering Practice Workflow

## 1. Mục tiêu
- Tự động hóa triển khai hạ tầng cloud (GCP VM, GCS bucket) bằng Terraform
- Build & run ETL pipeline với Docker
- Đọc dữ liệu từ GCS, xử lý và load vào BigQuery bằng Python
- Kiểm tra dữ liệu bằng SQL
- Tự động hóa toàn bộ quy trình với Makefile hoặc deploy.sh

## 2. Cấu trúc thư mục
```
Practice/
├── config/
│   └── gcp-service-account-key.json
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── etl/
│   └── etl.py
├── sql/
│   └── queries.sql
├── Makefile
├── deploy.sh
└── README.md
```

## 3. Hướng dẫn sử dụng

### A. Chuẩn bị
- Đặt file service account key GCP vào `config/gcp-service-account-key.json`
- Cài đặt: Terraform, Docker, Docker Compose, Python 3.9+

### B. Triển khai hạ tầng với Terraform
```sh
yarn global add terraform
cd terraform
yarn run terraform init
yarn run terraform apply -auto-approve
```

### C. Build & Run Docker
```sh
cd ../docker
yarn run docker build -t etl-app .
yarn run docker-compose up -d
```

### D. Chạy ETL pipeline
- Cấu hình biến môi trường: `GCS_BUCKET`, `BQ_DATASET`, `BQ_TABLE`
- Chạy ETL:
```sh
docker run --rm -e GCS_BUCKET=your-bucket -e BQ_DATASET=your-dataset -e BQ_TABLE=your-table etl-app
```

### E. Kiểm tra dữ liệu bằng SQL
- Sử dụng file `sql/queries.sql` để kiểm tra dữ liệu trên BigQuery hoặc PostgreSQL

### F. Tự động hóa toàn bộ quy trình
```sh
yarn run make all
# hoặc
bash deploy.sh
```

## 4. Cleanup
```sh
cd terraform
yarn run terraform destroy -auto-approve
```

## 5. Ghi chú
- Đảm bảo cấu hình đúng project, region, zone trong `terraform/variables.tf`
- Thay thế các giá trị placeholder trong Makefile, ETL script, queries.sql cho phù hợp với project của bạn 