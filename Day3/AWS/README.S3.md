# Học Amazon S3 với LocalStack

## 1. Giới thiệu về Amazon S3
Amazon Simple Storage Service (S3) là dịch vụ lưu trữ đối tượng của AWS, cho phép lưu trữ và truy xuất dữ liệu từ bất kỳ đâu trên web.

### 1.1. Các khái niệm cơ bản
- **Bucket**: Là container chứa các objects (files)
- **Object**: Là file và metadata của file đó
- **Key**: Là tên duy nhất của object trong bucket
- **Region**: Vị trí địa lý lưu trữ bucket

## 2. Cài đặt môi trường LocalStack
```bash
# Khởi động Docker container
docker run -d --name localstack-main -p 4566:4566 localstack/localstack

# Kích hoạt môi trường ảo
source venv/bin/activate
```

## 3. Làm việc với S3 Buckets

### 3.1. Tạo Bucket
```bash
# Tạo bucket mới
awslocal s3 mb s3://my-bucket

# Kiểm tra danh sách buckets
awslocal s3 ls
```

### 3.2. Upload Files
```bash
# Upload một file
awslocal s3 cp file.txt s3://my-bucket/

# Upload một thư mục
awslocal s3 cp my-folder/ s3://my-bucket/my-folder/ --recursive

# Upload với public access
awslocal s3 cp file.txt s3://my-bucket/ --acl public-read
```

### 3.3. Download Files
```bash
# Download một file
awslocal s3 cp s3://my-bucket/file.txt ./

# Download một thư mục
awslocal s3 cp s3://my-bucket/my-folder/ ./my-folder/ --recursive
```

### 3.4. Quản lý Files
```bash
# Liệt kê files trong bucket
awslocal s3 ls s3://my-bucket/

# Xóa file
awslocal s3 rm s3://my-bucket/file.txt

# Xóa nhiều files
awslocal s3 rm s3://my-bucket --recursive
```

## 4. Làm việc với S3 qua API

### 4.1. Endpoints
- **Base URL**: http://localhost:4566
- **Bucket URL**: http://localhost:4566/my-bucket
- **Object URL**: http://localhost:4566/my-bucket/file.txt

### 4.2. Ví dụ sử dụng curl
```bash
# Liệt kê buckets
curl http://localhost:4566/

# Liệt kê objects trong bucket
curl http://localhost:4566/my-bucket/

# Download file
curl http://localhost:4566/my-bucket/file.txt > downloaded.txt
```

## 5. Bài tập thực hành

### 5.1. Tạo Static Website
```bash
# 1. Tạo bucket
awslocal s3 mb s3://my-website

# 2. Upload files
echo "<html><body><h1>Hello AWS</h1></body></html>" > index.html
awslocal s3 cp index.html s3://my-website/

# 3. Truy cập website
curl http://localhost:4566/my-website/index.html
```

### 5.2. Quản lý Versions
```bash
# 1. Bật versioning
awslocal s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled

# 2. Upload nhiều versions
echo "v1" > file.txt
awslocal s3 cp file.txt s3://my-bucket/
echo "v2" > file.txt
awslocal s3 cp file.txt s3://my-bucket/

# 3. Liệt kê versions
awslocal s3api list-object-versions --bucket my-bucket
```

## 6. Xử lý lỗi thường gặp

### 6.1. NoSuchBucket
```bash
# Kiểm tra bucket tồn tại
awslocal s3 ls | grep my-bucket

# Tạo lại bucket nếu không tồn tại
awslocal s3 mb s3://my-bucket
```

### 6.2. Access Denied
```bash
# Kiểm tra ACL
awslocal s3api get-bucket-acl --bucket my-bucket

# Cấp quyền public
awslocal s3api put-bucket-acl --bucket my-bucket --acl public-read
```

## 7. Best Practices
1. **Naming Conventions**
   - Tên bucket phải unique
   - Chỉ sử dụng ký tự lowercase, số, dấu chấm và gạch ngang
   - Độ dài từ 3-63 ký tự

2. **Security**
   - Không để bucket public trừ khi cần thiết
   - Sử dụng IAM policies để quản lý quyền truy cập
   - Bật versioning cho dữ liệu quan trọng

3. **Performance**
   - Sử dụng prefix phù hợp cho key names
   - Tránh upload files quá lớn
   - Sử dụng multipart upload cho files lớn

## 8. Dọn dẹp môi trường
```bash
# Xóa tất cả objects trong bucket
awslocal s3 rm s3://my-bucket --recursive

# Xóa bucket
awslocal s3 rb s3://my-bucket

# Dừng container LocalStack
docker stop localstack-main

# Xóa container LocalStack
docker rm localstack-main

# Xóa image LocalStack (tùy chọn)
docker rmi localstack/localstack

# Deactivate môi trường ảo
deactivate
```

## 9. Tài liệu tham khảo
- [AWS S3 Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [LocalStack S3 API](https://docs.localstack.cloud/user-guide/aws/s3/)
- [AWS CLI S3 Commands](https://docs.aws.amazon.com/cli/latest/reference/s3/) 