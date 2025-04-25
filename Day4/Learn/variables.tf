variable "vpc_cidr" {
  description = "CIDR block cho VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "project_id" {
  description = "ID của GCP Project"
  type        = string
}

variable "environment" {
  description = "Môi trường deployment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "region" {
  description = "GCP Region để deploy resources"
  type        = string
  default     = "asia-southeast1"
}

variable "project_name" {
  description = "Tên project"
  type        = string
  default     = "data-engineering-practice"
}

variable "subnet_cidr" {
  description = "CIDR block cho subnet"
  type        = string
  default     = "10.0.0.0/24"
}
