# Data Engineering Infrastructure - GCP Terraform

Tự động hóa việc tạo infrastructure cho data engineering trên GCP sử dụng Terraform.

## Resources được tạo

- VPC Network & Subnet (asia-southeast1)
- Cloud Storage Bucket (Data Lake)
- BigQuery Dataset & Table

## Yêu cầu

1. Google Cloud SDK
2. Terraform
3. Service Account với các quyền:
   - Compute Network Admin
   - Storage Admin
   - BigQuery Admin

## Cách sử dụng

1. **Set credentials**:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

2. **Khởi tạo và tạo infrastructure**:
```bash
# Khởi tạo Terraform
terraform init

# Xem plan
terraform plan -var="project_id=your-project-id"

# Tạo infrastructure
terraform apply -var="project_id=your-project-id"
```

3. **Xóa infrastructure**:
```bash
terraform destroy -var="project_id=your-project-id"
```

## Cấu trúc

```
terraform-basics/
├── main.tf          # Resource definitions
├── variables.tf     # Input variables
└── outputs.tf       # Output values
```

## Biến

| Tên | Mặc định | Mô tả |
|-----|----------|-------|
| project_id | (required) | GCP Project ID |
| region | asia-southeast1 | Region để deploy |
| environment | dev | Môi trường (dev/staging/prod) |
| project_name | data-engineering-practice | Tên project |
| subnet_cidr | 10.0.0.0/24 | CIDR cho subnet |

## Outputs

- vpc_network_id: ID của VPC
- subnet_id: ID của subnet
- data_lake_bucket: Tên bucket
- bigquery_dataset: ID của dataset
- bigquery_table: ID của table

## Lưu ý

- KHÔNG commit file credentials
- Sử dụng biến môi trường cho credentials
- Kiểm tra kỹ plan trước khi apply 