# Học AWS IAM với LocalStack

## 1. Giới thiệu về IAM
IAM (Identity and Access Management) là dịch vụ quản lý quyền truy cập trong AWS:
- Users: Người dùng cuối
- Groups: Nhóm users
- Roles: Vai trò cho services
- Policies: Chính sách phân quyền

## 2. Thực hành với IAM

### 2.1. Tạo IAM User
```bash
# Tạo user mới
awslocal iam create-user --user-name myuser

# Tạo access key cho user
awslocal iam create-access-key --user-name myuser
```

### 2.2. Tạo IAM Group
```bash
# Tạo group
awslocal iam create-group --group-name developers

# Thêm user vào group
awslocal iam add-user-to-group --user-name myuser --group-name developers
```

### 2.3. Tạo IAM Policy
```bash
# Tạo policy cho phép đọc S3
cat << EOF > s3-read-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ]
        }
    ]
}
EOF

# Attach policy vào group
awslocal iam put-group-policy \
    --group-name developers \
    --policy-name S3ReadAccess \
    --policy-document file://s3-read-policy.json
```

### 2.4. Tạo IAM Role
```bash
# Tạo trust policy
cat << EOF > trust-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

# Tạo role
awslocal iam create-role \
    --role-name ec2-s3-role \
    --assume-role-policy-document file://trust-policy.json

# Attach policy vào role
awslocal iam put-role-policy \
    --role-name ec2-s3-role \
    --policy-name S3Access \
    --policy-document file://s3-read-policy.json
```

## 3. Best Practices
1. **Principle of Least Privilege**
   - Chỉ cấp quyền tối thiểu cần thiết
   - Thường xuyên review và thu hồi quyền không cần thiết

2. **Sử dụng Groups**
   - Quản lý users thông qua groups
   - Dễ dàng thêm/xóa quyền cho nhiều users

3. **Sử dụng Roles**
   - Dùng roles cho services thay vì access keys
   - Tăng tính bảo mật

4. **Monitoring và Audit**
   - Bật CloudTrail để log các API calls
   - Thường xuyên review access logs

## 4. Các lệnh hữu ích
```bash
# List users
awslocal iam list-users

# List groups
awslocal iam list-groups

# List roles
awslocal iam list-roles

# List policies của user
awslocal iam list-user-policies --user-name myuser

# List policies của group
awslocal iam list-group-policies --group-name developers

# Xóa user
awslocal iam delete-user --user-name myuser

# Xóa group
awslocal iam delete-group --group-name developers

# Xóa role
awslocal iam delete-role --role-name ec2-s3-role
``` 