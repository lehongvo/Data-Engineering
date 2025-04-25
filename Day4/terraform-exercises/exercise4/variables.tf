variable "project_id" {
  description = "The ID of the project"
  type        = string
  default     = "unique-axle-457602-n6"
}

variable "region" {
  description = "The region to deploy resources"
  type        = string
  default     = "asia-southeast1"
}

variable "zone" {
  description = "The zone to deploy resources"
  type        = string
  default     = "asia-southeast1-a"
}

variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "data-pipeline"
}

variable "environment" {
  description = "The environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# VPC Network Variables
variable "vpc_network_name" {
  description = "Name of the VPC network"
  type        = string
  default     = "dataflow-network"
}

variable "vpc_subnet_cidr" {
  description = "CIDR range for the VPC subnet"
  type        = string
  default     = "10.0.0.0/24"
}

# Storage Variables
variable "data_lake_storage_class" {
  description = "Storage class for the data lake bucket"
  type        = string
  default     = "STANDARD"
}

variable "temp_storage_class" {
  description = "Storage class for the temporary storage bucket"
  type        = string
  default     = "STANDARD"
}

variable "bucket_location" {
  description = "Location for the storage buckets"
  type        = string
  default     = "ASIA-SOUTHEAST1"
}

# Pub/Sub Variables
variable "topic_name" {
  description = "Name of the Pub/Sub topic"
  type        = string
  default     = "data-pipeline-topic"
}

variable "subscription_name" {
  description = "Name of the Pub/Sub subscription"
  type        = string
  default     = "data-pipeline-sub"
}

# Service Account Variables
variable "service_account_roles" {
  description = "List of roles to assign to the service account"
  type        = list(string)
  default = [
    "roles/dataflow.worker",
    "roles/storage.objectViewer",
    "roles/storage.objectCreator",
    "roles/pubsub.publisher",
    "roles/pubsub.subscriber",
    "roles/bigquery.dataEditor"
  ]
}

# Firewall Variables
variable "vpc_connector_range" {
  description = "IP range for the VPC connector"
  type        = string
  default     = "10.8.0.0/28"
}
