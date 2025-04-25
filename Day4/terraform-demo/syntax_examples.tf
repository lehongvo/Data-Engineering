# 1. Blocks và Arguments
# Block là container cho các cấu hình khác nhau
resource "google_compute_instance" "example" { # Block declaration
  name         = "example-instance"            # Argument
  machine_type = "e2-medium"                   # Argument
  zone         = "asia-southeast1-a"           # Argument

  # Block lồng nhau (Nested block)
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  # Block với nhiều item
  network_interface {
    network = "default"
    # Block có thể chứa các argument và block khác
    access_config {
      // Ephemeral public IP
    }
  }

  # List/Array argument
  tags = ["web", "dev"]

  # Map/Dictionary argument
  labels = {
    environment = "dev"
    team        = "engineering"
  }
}

# 2. Data Sources
# Dùng để query thông tin từ provider
data "google_compute_image" "debian" {
  family  = "debian-11"
  project = "debian-cloud"
}

# 3. Dependencies
# Implicit dependency (phụ thuộc ngầm định)
resource "google_compute_address" "static_ip" {
  name = "static-ip"
}

resource "google_compute_instance" "web" {
  name         = "web-instance"
  machine_type = "e2-medium"

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.static_ip.address # Implicit dependency
    }
  }
}

# 4. Explicit dependency (phụ thuộc tường minh)
resource "google_storage_bucket" "logs" {
  name     = "logging-bucket"
  location = "asia-southeast1"
}

resource "google_compute_instance" "app" {
  name         = "app-instance"
  machine_type = "e2-medium"

  depends_on = [google_storage_bucket.logs] # Explicit dependency
}

# 5. Count và For Each
# Sử dụng count để tạo nhiều resource giống nhau
resource "google_compute_instance" "cluster" {
  count        = 3
  name         = "node-${count.index}"
  machine_type = "e2-medium"
}

# Sử dụng for_each với map
resource "google_storage_bucket" "environments" {
  for_each = {
    dev  = "asia-southeast1"
    prod = "asia-southeast2"
  }

  name     = "bucket-${each.key}"
  location = each.value
}

# 6. Expressions
locals {
  instance_name = "app-${var.environment}"
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

# 7. Conditions
resource "google_compute_instance" "conditional" {
  name         = local.instance_name
  machine_type = var.environment == "prod" ? "e2-standard-2" : "e2-medium"

  tags = var.environment == "prod" ? ["prod", "web"] : ["dev", "web"]
}
