# 1. TERRAFORM STATE CONFIGURATION
terraform {
  # Backend configuration - Lưu state file trên Google Cloud Storage
  backend "gcs" {
    bucket = "terraform-state-demo"
    prefix = "terraform/state"
  }

  # Có thể thay thế bằng các backend khác như:
  # backend "local" {} - Lưu locally (default)
  # backend "s3" {}    - Lưu trên AWS S3
  # backend "azurerm" {} - Lưu trên Azure Storage
}

# 2. RESOURCE EXAMPLE
resource "google_storage_bucket" "state_demo" {
  name     = "demo-bucket-state"
  location = "asia-southeast1"

  # Versioning để tracking thay đổi
  versioning {
    enabled = true
  }

  # Lifecycle rules
  lifecycle_rule {
    condition {
      age = 30 # 30 days
    }
    action {
      type = "Delete"
    }
  }
}

# 3. DATA SOURCE - Đọc state của resource khác
data "terraform_remote_state" "network" {
  backend = "gcs"

  config = {
    bucket = "terraform-state-demo"
    prefix = "terraform/network"
  }
}

# 4. USING REMOTE STATE DATA
resource "google_compute_instance" "app" {
  name         = "app-instance"
  machine_type = "e2-medium"
  zone         = "asia-southeast1-a"

  # Sử dụng thông tin từ remote state
  network_interface {
    network    = data.terraform_remote_state.network.outputs.network_name
    subnetwork = data.terraform_remote_state.network.outputs.subnet_name
  }

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
}

# 5. STATE LOCKING
# GCS tự động hỗ trợ state locking
# Có thể cấu hình custom lock provider:
terraform {
  backend "gcs" {
    bucket = "terraform-state-demo"
    prefix = "terraform/state"

    # Custom lock settings nếu cần
    enable_lock = true
    lock_table  = "terraform_locks"
  }
}

# 6. WORKSPACE SUPPORT
# Các workspace khác nhau sẽ có state files khác nhau
# Ví dụ: terraform workspace new dev
# State file sẽ được lưu tại: terraform/state/dev/terraform.tfstate

# 7. OUTPUT FOR STATE SHARING
output "bucket_name" {
  value       = google_storage_bucket.state_demo.name
  description = "Name of the created bucket - có thể được sử dụng bởi các module khác"
}

# 8. IMPORT EXISTING RESOURCES
# Sử dụng lệnh: terraform import google_storage_bucket.state_demo bucket-name

# 9. STATE MANAGEMENT COMMANDS
# terraform state list
# terraform state show google_storage_bucket.state_demo
# terraform state mv
# terraform state rm
# terraform state pull
# terraform state push 
