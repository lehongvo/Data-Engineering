# AWS Introduction - Học AWS từ cơ bản

## 1. Giới thiệu về AWS
Amazon Web Services (AWS) là nền tảng điện toán đám mây hàng đầu, cung cấp hơn 200 dịch vụ đầy đủ tính năng từ các trung tâm dữ liệu trên toàn cầu.

### Các dịch vụ cốt lõi của AWS:

1. **EC2 (Elastic Compute Cloud)**
   - Dịch vụ máy chủ ảo
   - Cho phép chạy các ứng dụng trên đám mây
   - Có thể mở rộng hoặc thu nhỏ theo nhu cầu

2. **S3 (Simple Storage Service)**
   - Dịch vụ lưu trữ đối tượng
   - Lưu trữ và truy xuất dữ liệu từ bất kỳ đâu
   - Độ bền và khả năng mở rộng cao

3. **IAM (Identity and Access Management)**
   - Quản lý người dùng và quyền truy cập
   - Kiểm soát bảo mật cho tài khoản AWS
   - Xác thực và phân quyền

## 2. Các bước thiết lập tài khoản AWS Free Tier

1. **Đăng ký tài khoản AWS**
   - Truy cập aws.amazon.com
   - Click "Create an AWS Account"
   - Điền thông tin cá nhân và thanh toán
   - Xác minh số điện thoại

2. **Thiết lập bảo mật**
   - Bật xác thực hai yếu tố (MFA)
   - Tạo IAM user thay vì sử dụng root account
   - Thiết lập mật khẩu mạnh

3. **Tìm hiểu về Free Tier**
   - 12 tháng sử dụng miễn phí
   - Giới hạn sử dụng cho mỗi dịch vụ
   - Theo dõi việc sử dụng để tránh phát sinh chi phí

## 3. Các bước thực hành tiếp theo

1. Tạo EC2 instance
2. Tạo S3 bucket
3. Thiết lập IAM user và policy
4. Kết nối với AWS CLI

## Lưu ý quan trọng
- Luôn theo dõi việc sử dụng tài nguyên
- Tắt các dịch vụ không sử dụng
- Đặt cảnh báo chi phí
- Tuân thủ các nguyên tắc bảo mật 

# Học AWS với LocalStack

## 1. Giới thiệu
LocalStack là công cụ mô phỏng các dịch vụ AWS trên máy tính local, giúp bạn học và phát triển ứng dụng AWS mà không cần tài khoản AWS thật.

## 2. Cài đặt môi trường

### 2.1. Cài đặt Docker Desktop
1. Truy cập: https://www.docker.com/products/docker-desktop
2. Tải phiên bản phù hợp với hệ điều hành
3. Cài đặt và khởi động Docker Desktop

### 2.2. Cài đặt Python và pip
1. Tải Python: https://www.python.org/downloads/
2. Kiểm tra cài đặt:
   ```bash
   python3 --version
   pip3 --version
   ```

### 2.3. Thiết lập môi trường ảo (Virtual Environment)
```bash
# Tạo môi trường ảo
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2.4. Cài đặt LocalStack và AWS CLI local
```bash
# Cài đặt các package cần thiết
pip install localstack awscli-local

# Kiểm tra cài đặt
localstack --version
awslocal --version
```

## 3. Khởi động LocalStack

### 3.1. Sử dụng Docker trực tiếp (Khuyến nghị)
```bash
# Tải image
docker pull localstack/localstack

# Chạy container
docker run -d --name localstack-main -p 4566:4566 localstack/localstack
```

### 3.2. Kiểm tra trạng thái
```bash
# Kiểm tra container
docker ps | grep localstack

# Kiểm tra health check
curl http://localhost:4566/_localstack/health
```

## 4. Sử dụng các dịch vụ AWS

### 4.1. S3 (Simple Storage Service)
```bash
# Tạo bucket
awslocal s3 mb s3://my-bucket

# Upload file
awslocal s3 cp file.txt s3://my-bucket/

# Liệt kê files
awslocal s3 ls s3://my-bucket
```

### 4.2. EC2 (Elastic Compute Cloud)
```bash
# Tạo EC2 instance
awslocal ec2 run-instances --image-id ami-123 --instance-type t2.micro

# Liệt kê instances
awslocal ec2 describe-instances

# Dừng instance
awslocal ec2 stop-instances --instance-ids i-1234567890abcdef0
```

### 4.3. IAM (Identity and Access Management)
```bash
# Tạo user
awslocal iam create-user --user-name testuser

# Tạo policy
awslocal iam create-policy --policy-name TestPolicy --policy-document file://policy.json

# Gán policy cho user
awslocal iam attach-user-policy --user-name testuser --policy-arn arn:aws:iam::000000000000:policy/TestPolicy
```

## 5. Endpoints quan trọng

- Health Check: http://localhost:4566/_localstack/health
- S3 Endpoint: http://localhost:4566/s3
- EC2 Endpoint: http://localhost:4566/ec2
- IAM Endpoint: http://localhost:4566/iam

## 6. Lưu ý quan trọng

1. **Dữ liệu sẽ bị mất khi restart**
   - LocalStack không lưu dữ liệu vĩnh viễn
   - Cần tạo lại resources sau mỗi lần khởi động lại

2. **Sử dụng awslocal thay vì aws**
   - `awslocal` là wrapper cho AWS CLI
   - Tự động điều hướng đến LocalStack endpoint

3. **Port mặc định**
   - LocalStack sử dụng port 4566
   - Đảm bảo port không bị conflict

4. **Môi trường ảo**
   - Luôn kích hoạt môi trường ảo trước khi sử dụng
   - `source venv/bin/activate`

## 7. Khắc phục sự cố

1. **Nếu LocalStack không khởi động**
   ```bash
   # Dừng container cũ
   docker stop localstack-main
   docker rm localstack-main
   
   # Chạy container mới
   docker run -d --name localstack-main -p 4566:4566 localstack/localstack
   ```

2. **Nếu lệnh awslocal không hoạt động**
   ```bash
   # Kích hoạt lại môi trường ảo
   source venv/bin/activate
   
   # Cài đặt lại awscli-local
   pip install awscli-local
   ```

## 8. Tài liệu tham khảo

- LocalStack Documentation: https://docs.localstack.cloud
- AWS CLI Documentation: https://aws.amazon.com/cli/
- Docker Documentation: https://docs.docker.com 