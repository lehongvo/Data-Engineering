#!/bin/bash

# Output colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Message display functions
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check required tools
check_requirements() {
    print_message "Checking required tools..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    # Check awslocal
    if ! command -v awslocal &> /dev/null; then
        print_error "awslocal is not installed. Please run: pip install awscli-local"
        exit 1
    fi
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Initialize clean environment
init_environment() {
    print_warning "Cleaning up old environment..."
    
    # Stop running container if exists
    if [ "$(docker ps -q -f name=localstack-main)" ]; then
        print_message "Stopping running localstack-main container..."
        docker stop localstack-main
    fi
    
    # Remove old container if exists
    if [ "$(docker ps -aq -f name=localstack-main)" ]; then
        print_message "Removing old localstack-main container..."
        docker rm localstack-main
    fi
    
    print_message "Environment cleaned"
}

# Start LocalStack
start_localstack() {
    print_message "Starting LocalStack..."
    docker run -d --name localstack-main -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
    
    # Wait for LocalStack to be ready
    print_message "Waiting for LocalStack to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s localhost:4566 > /dev/null; then
            print_message "LocalStack is ready"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_error "LocalStack failed to start after ${max_attempts} seconds"
    cleanup
    exit 1
}

# Create key pair
create_key_pair() {
    if [ -z "$1" ]; then
        print_error "Please provide a key pair name"
        return 1
    fi
    
    print_message "Creating key pair $1..."
    if awslocal ec2 create-key-pair --key-name "$1" --query 'KeyMaterial' --output text > "$1.pem"; then
        chmod 400 "$1.pem"
        print_message "Key pair created and saved to $1.pem"
    else
        print_error "Failed to create key pair"
        return 1
    fi
}

# Create security group
create_security_group() {
    if [ -z "$1" ]; then
        print_error "Please provide a security group name"
        return 1
    fi
    
    print_message "Creating security group $1..."
    if awslocal ec2 create-security-group --group-name "$1" --description "Security group for EC2"; then
        print_message "Adding SSH rule..."
        awslocal ec2 authorize-security-group-ingress \
            --group-name "$1" \
            --protocol tcp \
            --port 22 \
            --cidr 0.0.0.0/0
        
        print_message "Adding HTTP rule..."
        awslocal ec2 authorize-security-group-ingress \
            --group-name "$1" \
            --protocol tcp \
            --port 80 \
            --cidr 0.0.0.0/0
            
        print_message "Security group created successfully"
    else
        print_error "Failed to create security group"
        return 1
    fi
}

# Create user data script
create_user_data() {
    print_message "Creating user data script..."
    cat << 'EOF' > user-data.sh
#!/bin/bash
yum update -y
yum install -y httpd

# Start and enable Apache
systemctl start httpd
systemctl enable httpd

# Create index.html with our content
cat << 'EOH' > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My EC2 Web Server</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        background: #f0f2f5;
      }
      .container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      h1 {
        color: #1a73e8;
        text-align: center;
      }
      p {
        line-height: 1.6;
        color: #333;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Welcome to My EC2 Web Server</h1>
      <p>
        This page is being served from an EC2 instance running on LocalStack!
      </p>
      <p>Server Status: Running</p>
      <p>Time: <span id="time"></span></p>
    </div>
    <script>
      function updateTime() {
        document.getElementById("time").textContent =
          new Date().toLocaleString();
      }
      updateTime();
      setInterval(updateTime, 1000);
    </script>
  </body>
</html>
EOH
EOF
    chmod +x user-data.sh
    print_message "User data script created successfully"
}

# Launch EC2 instance
launch_instance() {
    if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
        print_error "Please provide: key pair name, security group ID, and instance name"
        return 1
    fi
    
    # Create user data script first
    create_user_data
    
    print_message "Launching EC2 instance..."
    local instance_id=$(awslocal ec2 run-instances \
        --image-id ami-0c55b159cbfafe1f0 \
        --instance-type t2.micro \
        --key-name "$1" \
        --security-group-ids "$2" \
        --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$3}]" \
        --user-data file://user-data.sh \
        --query 'Instances[0].InstanceId' \
        --output text)
    
    if [ $? -eq 0 ]; then
        print_message "Instance launched successfully"
        print_message "Instance ID: $instance_id"
        
        # Get the public IP address
        local public_ip=$(awslocal ec2 describe-instances \
            --instance-ids "$instance_id" \
            --query 'Reservations[0].Instances[0].PublicIpAddress' \
            --output text)
        
        print_message "Public IP: $public_ip"
        print_message "Web server will be available at: http://$public_ip"
        print_message "Please wait a few minutes for the web server to start"
    else
        print_error "Failed to launch instance"
        return 1
    fi
}

# List instances
list_instances() {
    print_message "Listing EC2 instances..."
    awslocal ec2 describe-instances \
        --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' \
        --output table
}

# Stop instance
stop_instance() {
    if [ -z "$1" ]; then
        print_error "Please provide instance ID"
        return 1
    fi
    
    print_message "Stopping instance $1..."
    if awslocal ec2 stop-instances --instance-ids "$1"; then
        print_message "Instance stopped successfully"
    else
        print_error "Failed to stop instance"
        return 1
    fi
}

# Start instance
start_instance() {
    if [ -z "$1" ]; then
        print_error "Please provide instance ID"
        return 1
    fi
    
    print_message "Starting instance $1..."
    if awslocal ec2 start-instances --instance-ids "$1"; then
        print_message "Instance started successfully"
    else
        print_error "Failed to start instance"
        return 1
    fi
}

# Terminate instance
terminate_instance() {
    if [ -z "$1" ]; then
        print_error "Please provide instance ID"
        return 1
    fi
    
    print_warning "Terminating instance $1..."
    if awslocal ec2 terminate-instances --instance-ids "$1"; then
        print_message "Instance terminated successfully"
    else
        print_error "Failed to terminate instance"
        return 1
    fi
}

# Clean up environment
cleanup() {
    print_warning "Cleaning up environment..."
    if [ "$(docker ps -q -f name=localstack-main)" ]; then
        docker stop localstack-main
        docker rm localstack-main
    fi
    print_message "Cleanup complete"
}

# Show menu
show_menu() {
    echo -e "\n${GREEN}=== EC2 MANAGEMENT MENU ===${NC}"
    echo "1. Start LocalStack"
    echo "2. Create Key Pair"
    echo "3. Create Security Group"
    echo "4. Launch EC2 Instance"
    echo "5. List Instances"
    echo "6. Start Instance"
    echo "7. Stop Instance"
    echo "8. Terminate Instance"
    echo "9. Clean Environment"
    echo "0. Exit"
    echo -n "Your choice: "
}

# Main loop
main() {
    check_requirements
    check_docker
    init_environment
    
    while true; do
        show_menu
        read choice
        case $choice in
            1) start_localstack ;;
            2)
                echo -n "Enter key pair name: "
                read key_name
                create_key_pair "$key_name"
                ;;
            3)
                echo -n "Enter security group name: "
                read sg_name
                create_security_group "$sg_name"
                ;;
            4)
                echo -n "Enter key pair name: "
                read key_name
                echo -n "Enter security group ID (e.g. sg-xxx): "
                read sg_id
                echo -n "Enter instance name: "
                read instance_name
                launch_instance "$key_name" "$sg_id" "$instance_name"
                ;;
            5) list_instances ;;
            6)
                echo -n "Enter instance ID: "
                read instance_id
                start_instance "$instance_id"
                ;;
            7)
                echo -n "Enter instance ID: "
                read instance_id
                stop_instance "$instance_id"
                ;;
            8)
                echo -n "Enter instance ID: "
                read instance_id
                terminate_instance "$instance_id"
                ;;
            9)
                cleanup
                init_environment
                ;;
            0)
                cleanup
                print_message "Goodbye!"
                exit 0
                ;;
            *) print_error "Invalid choice" ;;
        esac
    done
}

# Run script
main 