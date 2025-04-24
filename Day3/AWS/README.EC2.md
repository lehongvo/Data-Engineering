# Học Amazon EC2 với LocalStack

## 1. Giới thiệu về Amazon EC2
Amazon Elastic Compute Cloud (EC2) là dịch vụ cung cấp máy chủ ảo trong môi trường điện toán đám mây AWS.

### 1.1. Các khái niệm cơ bản
- **Instance**: Máy chủ ảo trong EC2
- **AMI (Amazon Machine Image)**: Template để tạo instance
- **Instance Type**: Cấu hình phần cứng của instance
- **Security Group**: Tường lửa ảo cho instance
- **Key Pair**: Cặp khóa để SSH vào instance

## 2. Làm việc với EC2 trên LocalStack

### 2.1. Khởi tạo môi trường
```bash
# Khởi động LocalStack
docker run -d --name localstack-main -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
```

### 2.2. Tạo Key Pair
```bash
# Tạo key pair mới
awslocal ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > MyKeyPair.pem

# Phân quyền cho file key
chmod 400 MyKeyPair.pem
```

### 2.3. Tạo Security Group
```bash
# Tạo security group
awslocal ec2 create-security-group --group-name MySecurityGroup --description "My security group"

# Thêm rule cho phép SSH
awslocal ec2 authorize-security-group-ingress \
    --group-name MySecurityGroup \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
```

### 2.4. Khởi tạo EC2 Instance
```bash
# Tạo EC2 instance
awslocal ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name MyKeyPair \
    --security-group-ids MySecurityGroup \
    --count 1

# Liệt kê instances
awslocal ec2 describe-instances
```

### 2.5. Quản lý Instance
```bash
# Start instance
awslocal ec2 start-instances --instance-ids i-1234567890abcdef0

# Stop instance
awslocal ec2 stop-instances --instance-ids i-1234567890abcdef0

# Terminate instance
awslocal ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

## 3. Thực hành với EC2

### 3.1. Deploy Web Server
```bash
# Tạo user data script
cat << 'EOF' > user-data.sh
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from LocalStack EC2!</h1>" > /var/www/html/index.html
EOF

# Tạo instance với user data
awslocal ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name MyKeyPair \
    --security-group-ids MySecurityGroup \
    --user-data file://user-data.sh
```

### 3.2. Tạo và Gắn EBS Volume
```bash
# Tạo EBS volume
awslocal ec2 create-volume \
    --size 10 \
    --availability-zone us-east-1a

# Gắn volume vào instance
awslocal ec2 attach-volume \
    --volume-id vol-1234567890abcdef0 \
    --instance-id i-1234567890abcdef0 \
    --device /dev/sdf
```

## 4. Best Practices
1. **Security**
   - Sử dụng security groups hợp lý
   - Chỉ mở các ports cần thiết
   - Luôn sử dụng key pairs cho SSH

2. **Storage**
   - Sử dụng EBS volumes cho dữ liệu quan trọng
   - Thực hiện backup thường xuyên
   - Chọn đúng loại storage cho use case

3. **Monitoring**
   - Theo dõi CPU, memory usage
   - Set up alerts cho các metrics quan trọng
   - Kiểm tra logs thường xuyên

## 5. Troubleshooting
1. **Instance không start được**
   - Kiểm tra security group
   - Kiểm tra key pair
   - Xem logs của instance

2. **Không thể kết nối SSH**
   - Kiểm tra inbound rules trong security group
   - Kiểm tra key pair permissions
   - Kiểm tra network connectivity 