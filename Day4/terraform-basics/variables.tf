variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "region" {
  description = "The region to deploy resources to"
  type        = string
  default     = "asia-southeast1"
}

variable "environment" {
  description = "The environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "data-engineering-practice"
}

variable "subnet_cidr" {
  description = "The CIDR block for the subnet"
  type        = string
  default     = "10.0.0.0/24"
}

variable "instance_name" {
  description = "The name of the VM instance"
  type        = string
  default     = "data-processing-instance"
}

variable "machine_type" {
  description = "The machine type of the VM instance"
  type        = string
  default     = "e2-medium"
}

variable "zone" {
  description = "The zone where the VM instance will be created"
  type        = string
  default     = "asia-southeast1-a"
}

variable "instance_tags" {
  description = "Network tags for the VM instance"
  type        = list(string)
  default     = ["data-processing"]
}
