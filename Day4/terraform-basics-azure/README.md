# Terraform Azure Basic Setup

This repository contains basic Terraform configuration for Azure. This setup is for learning purposes using Microsoft Learn resources.

## Prerequisites

1. Install Terraform
```bash
brew install terraform    # For MacOS
```

2. Install Azure CLI
```bash
brew install azure-cli   # For MacOS
```

3. Login to Azure (using Microsoft Learn sandbox if available)
```bash
az login
```

## Project Structure
```
.
├── README.md
├── main.tf         # Main Terraform configuration
├── variables.tf    # Variable definitions
├── outputs.tf      # Output definitions
└── .gitignore     # Git ignore file
```

## Getting Started

1. Initialize Terraform:
```bash
terraform init
```

2. Plan your changes:
```bash
terraform plan
```

3. Apply the changes:
```bash
terraform apply
```

4. When finished, destroy resources:
```bash
terraform destroy
```

## Note
This setup is intended for learning purposes using Microsoft Learn resources. For production environments, please ensure proper authentication and resource management. 