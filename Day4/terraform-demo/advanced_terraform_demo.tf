# 1. MODULES
# ./modules/gce-instance/main.tf
module "web_server" {
  source = "./modules/gce-instance"

  instance_name = "web-server"
  machine_type  = "e2-medium"
  zone          = "asia-southeast1-a"

  # Version constraint
  version = "~> 1.0.0"
}

# 2. DYNAMIC BLOCKS
resource "google_compute_instance" "dynamic_example" {
  name         = "dynamic-example"
  machine_type = "e2-medium"

  dynamic "service_account" {
    for_each = var.service_accounts
    content {
      email  = service_account.value.email
      scopes = service_account.value.scopes
    }
  }
}

# 3. PROVIDER CONFIGURATIONS
provider "google" {
  alias   = "asia"
  region  = "asia-southeast1"
  project = "project-asia"
}

provider "google" {
  alias   = "europe"
  region  = "europe-west1"
  project = "project-europe"
}

# Sử dụng provider cụ thể
resource "google_compute_instance" "asia_instance" {
  provider = google.asia
  # ... other configurations
}

# 4. COUNT VÀ FOR_EACH NÂNG CAO
# Sử dụng count với conditional
resource "google_compute_instance" "conditional_servers" {
  count = var.environment == "prod" ? 3 : 1
  name  = "server-${count.index}"
  # ... other configurations
}

# Sử dụng for_each với dynamic values
resource "google_compute_instance" "map_servers" {
  for_each = {
    for idx, config in var.server_configs :
    config.name => config
    if config.enabled
  }

  name         = each.key
  machine_type = each.value.machine_type
  zone         = each.value.zone
}

# 5. CUSTOM CONDITIONS VÀ VALIDATIONS
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# 6. LIFECYCLE RULES NÂNG CAO
resource "google_storage_bucket" "advanced_lifecycle" {
  name     = "advanced-lifecycle-bucket"
  location = "asia-southeast1"

  lifecycle {
    prevent_destroy = true
    ignore_changes = [
      labels,
      lifecycle_rule
    ]
    create_before_destroy = true
  }
}

# 7. DATA SOURCES VÀ DYNAMIC FILTERING
data "google_compute_zones" "available" {
  project = var.project_id
  region  = var.region

  status = "UP"
}

# 8. LOCAL-EXEC PROVISIONER
resource "null_resource" "deployment" {
  triggers = {
    instance_ids = join(",", google_compute_instance.cluster[*].id)
  }

  provisioner "local-exec" {
    command = "echo 'Deployment completed for instances: ${self.triggers.instance_ids}'"
  }
}

# 9. TERRAFORM FUNCTIONS
locals {
  # String manipulation
  instance_name = lower(format("%s-%s-%s", var.project, var.environment, var.name))

  # List manipulation
  all_tags = distinct(concat(var.common_tags, var.environment_tags))

  # Map manipulation
  merged_labels = merge(
    var.common_labels,
    var.environment_labels,
    {
      terraform_managed = "true"
      timestamp         = timestamp()
    }
  )
}

# 10. CONDITIONAL EXPRESSIONS NÂNG CAO
locals {
  instance_config = {
    machine_type = var.environment == "prod" ? "e2-standard-4" : "e2-medium"

    disk_size = (
      var.environment == "prod" ? 100 :
      var.environment == "staging" ? 50 :
      20
    )

    backup_enabled = contains(["prod", "staging"], var.environment)
  }
}

# 11. ERROR HANDLING
resource "google_compute_instance" "error_handled" {
  name         = var.instance_name
  machine_type = var.machine_type

  boot_disk {
    initialize_params {
      image = try(
        data.google_compute_image.custom_image.self_link,
        data.google_compute_image.default_image.self_link
      )
    }
  }
}

# 12. WORKSPACES MANAGEMENT
locals {
  workspace_config = {
    dev = {
      instance_count = 1
      machine_type   = "e2-medium"
    }
    staging = {
      instance_count = 2
      machine_type   = "e2-standard-2"
    }
    prod = {
      instance_count = 3
      machine_type   = "e2-standard-4"
    }
  }

  current_config = local.workspace_config[terraform.workspace]
}
