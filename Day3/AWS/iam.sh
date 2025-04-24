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

# Create IAM User
create_user() {
    if [ -z "$1" ]; then
        print_error "Please provide a username"
        return 1
    fi
    
    print_message "Creating IAM user $1..."
    if awslocal iam create-user --user-name "$1"; then
        print_message "Creating access key for $1..."
        awslocal iam create-access-key --user-name "$1"
        print_message "User created successfully"
    else
        print_error "Failed to create user"
        return 1
    fi
}

# Create IAM Group
create_group() {
    if [ -z "$1" ]; then
        print_error "Please provide a group name"
        return 1
    fi
    
    print_message "Creating IAM group $1..."
    if awslocal iam create-group --group-name "$1"; then
        print_message "Group created successfully"
    else
        print_error "Failed to create group"
        return 1
    fi
}

# Add user to group
add_user_to_group() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        print_error "Please provide both username and group name"
        return 1
    fi
    
    print_message "Adding user $1 to group $2..."
    if awslocal iam add-user-to-group --user-name "$1" --group-name "$2"; then
        print_message "User added to group successfully"
    else
        print_error "Failed to add user to group"
        return 1
    fi
}

# Create S3 read policy
create_s3_policy() {
    print_message "Creating S3 read policy..."
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
    print_message "Policy file created successfully"
}

# Create EC2 trust policy
create_trust_policy() {
    print_message "Creating trust policy..."
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
    print_message "Trust policy file created successfully"
}

# Create IAM Role
create_role() {
    if [ -z "$1" ]; then
        print_error "Please provide a role name"
        return 1
    fi
    
    create_trust_policy
    print_message "Creating IAM role $1..."
    if awslocal iam create-role --role-name "$1" --assume-role-policy-document file://trust-policy.json; then
        create_s3_policy
        print_message "Attaching S3 policy to role..."
        awslocal iam put-role-policy \
            --role-name "$1" \
            --policy-name S3Access \
            --policy-document file://s3-read-policy.json
        print_message "Role created successfully"
    else
        print_error "Failed to create role"
        return 1
    fi
}

# List IAM resources
list_resources() {
    print_message "Listing IAM Users:"
    awslocal iam list-users
    
    print_message "\nListing IAM Groups:"
    awslocal iam list-groups
    
    print_message "\nListing IAM Roles:"
    awslocal iam list-roles
}

# Show menu
show_menu() {
    echo -e "\n${GREEN}=== IAM MANAGEMENT MENU ===${NC}"
    echo "1. Create IAM User"
    echo "2. Create IAM Group"
    echo "3. Add User to Group"
    echo "4. Create IAM Role"
    echo "5. List Resources"
    echo "0. Exit"
    echo -n "Your choice: "
}

# Main loop
main() {
    while true; do
        show_menu
        read choice
        case $choice in
            1)
                echo -n "Enter username: "
                read username
                create_user "$username"
                ;;
            2)
                echo -n "Enter group name: "
                read groupname
                create_group "$groupname"
                ;;
            3)
                echo -n "Enter username: "
                read username
                echo -n "Enter group name: "
                read groupname
                add_user_to_group "$username" "$groupname"
                ;;
            4)
                echo -n "Enter role name: "
                read rolename
                create_role "$rolename"
                ;;
            5)
                list_resources
                ;;
            0)
                print_message "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid choice"
                ;;
        esac
    done
}

# Run script
main 