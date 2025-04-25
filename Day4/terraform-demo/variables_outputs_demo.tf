# 1. VARIABLES - Các kiểu khai báo biến
# String variable
variable "instance_name" {
  type        = string
  default     = "my-instance"
  description = "The name of the instance"
}

# Number variable
variable "instance_count" {
  type        = number
  default     = 2
  description = "Number of instances to create"
}

# Boolean variable
variable "is_production" {
  type        = bool
  default     = false
  description = "Whether this is a production environment"
}

# List variable
variable "allowed_ports" {
  type        = list(number)
  default     = [80, 443, 8080]
  description = "List of allowed ports"
}

# Map variable
variable "instance_tags" {
  type = map(string)
  default = {
    environment = "dev"
    team        = "devops"
    project     = "demo"
  }
  description = "Tags to apply to instances"
}

# Object variable
variable "instance_config" {
  type = object({
    machine_type = string
    zone         = string
    labels       = map(string)
    tags         = list(string)
  })
  default = {
    machine_type = "e2-medium"
    zone         = "asia-southeast1-a"
    labels = {
      environment = "dev"
    }
    tags = ["web", "app"]
  }
  description = "Configuration for the instance"
}

# Set variable (unique values)
variable "unique_tags" {
  type        = set(string)
  default     = ["web", "app", "db"]
  description = "Unique tags for the instance"
}

# Tuple variable (fixed-length list with mixed types)
variable "instance_details" {
  type        = tuple([string, number, bool])
  default     = ["e2-medium", 1, true]
  description = "Instance details as [type, count, is_public]"
}

# 2. OUTPUTS - Các kiểu output
# Simple output
output "instance_name" {
  value       = var.instance_name
  description = "The name of the instance"
}

# Output with condition
output "environment_info" {
  value       = var.is_production ? "PRODUCTION" : "DEVELOPMENT"
  description = "Current environment information"
}

# Output from a map
output "team_info" {
  value       = var.instance_tags["team"]
  description = "Team responsible for the instance"
}

# Complex output with multiple values
output "instance_details" {
  value = {
    name         = var.instance_name
    machine_type = var.instance_config.machine_type
    is_prod      = var.is_production
    ports        = var.allowed_ports
  }
  description = "All instance details"
  sensitive   = false # Set to true for sensitive data
}

# Output with data transformation
output "allowed_ports_string" {
  value       = join(", ", var.allowed_ports)
  description = "Comma-separated list of allowed ports"
}

# 3. USING VARIABLES IN RESOURCES
resource "google_compute_instance" "example" {
  name         = var.instance_name
  machine_type = var.instance_config.machine_type
  zone         = var.instance_config.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }

  labels = var.instance_config.labels
  tags   = var.instance_config.tags

  metadata = {
    environment = var.is_production ? "prod" : "dev"
  }
} 
