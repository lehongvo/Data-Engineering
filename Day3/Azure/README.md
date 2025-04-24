# Azure VM Demo Project

## Giới Thiệu
Dự án này demo việc triển khai một trang web đơn giản trên Azure Virtual Machine, sử dụng Ubuntu Server và Nginx.

## Thông Tin Triển Khai
- **VM Name**: test-de-vincent
- **Resource Group**: learn-e9378c0f-90ca-46cf-87f4-c793adf3c9f2
- **Region**: East US
- **Public IP**: 52.234.122.148
- **OS**: Ubuntu 24.04.2 LTS
- **Web Server**: Nginx

## Cấu Trúc Project
```
.
├── README.md
├── index.html      # Trang web chính với modern UI
└── vincent.pem     # SSH private key (không được commit)
```

## Tính Năng Website
1. **Modern UI/UX**
   - Gradient background
   - Card-based layout
   - Hover effects
   - Responsive design
   - Fade-in animations

2. **Technical Features**
   - HTML5 & CSS3
   - Flexbox & Grid layout
   - Mobile-first approach
   - Cross-browser compatibility

## Hướng Dẫn Cài Đặt

### 1. Chuẩn Bị
- Azure Account (có thể dùng free tier)
- SSH client
- Terminal/Command Prompt

### 2. Tạo VM trên Azure
```bash
# Login vào Azure
az login

# Tạo VM
az vm create \
  --resource-group "learn-sandbox" \
  --name "test-de-vincent" \
  --image "Ubuntu2204" \
  --admin-username "azureuser" \
  --generate-ssh-keys \
  --size "Standard_B1s"
```

### 3. Cài Đặt Web Server
```bash
# SSH vào VM
ssh -i vincent.pem azureuser@52.234.122.148

# Cài đặt Nginx
sudo apt update
sudo apt install -y nginx
```

### 4. Deploy Website
```bash
# Upload file HTML
scp -i vincent.pem index.html azureuser@52.234.122.148:/home/azureuser/

# Di chuyển file vào web root
sudo mv /home/azureuser/index.html /var/www/html/
sudo chown www-data:www-data /var/www/html/index.html
```

## Bảo Mật
1. **Network Security Group Rules**
   - Port 22 (SSH): Allowed
   - Port 80 (HTTP): Allowed
   - Các port khác: Blocked

2. **SSH Security**
   - Sử dụng key-based authentication
   - Disable password authentication
   - Regular key rotation recommended

## Monitoring
- Azure Monitor enabled
- Resource metrics tracking
- Performance monitoring
- Security alerts

## Maintenance
1. **Regular Updates**
```bash
sudo apt update
sudo apt upgrade
```

2. **Backup**
   - Tạo VM snapshots
   - Backup website content
   - Store SSH keys safely

## Troubleshooting
1. **Cannot SSH**
   - Kiểm tra NSG rules
   - Verify SSH key permissions (chmod 400)
   - Check VM status

2. **Website Not Loading**
   - Verify Nginx status: `sudo systemctl status nginx`
   - Check error logs: `sudo tail -f /var/log/nginx/error.log`
   - Verify firewall rules

## Chi Phí
- VM size: Standard_B1s (economical choice)
- Estimated monthly cost: ~$20-30 USD
- Cost optimization tips:
  - Stop VM when not in use
  - Use auto-shutdown
  - Monitor resource usage

## Liên Hệ & Hỗ Trợ
- Author: Vincent
- Project Status: Demo/Learning
- Documentation: [Azure VM Docs](https://docs.microsoft.com/azure/virtual-machines/)

## License
MIT License - Feel free to use for learning purposes 