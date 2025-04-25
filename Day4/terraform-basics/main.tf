terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Tạo VPC
resource "google_compute_network" "vpc" {
  name                    = "${var.project_name}-vpc"
  auto_create_subnetworks = false
}

# Tạo Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_name}-subnet"
  ip_cidr_range = var.subnet_cidr
  network       = google_compute_network.vpc.id
  region        = var.region
}

# Tạo Cloud Storage bucket (tương đương với S3)
resource "google_storage_bucket" "data_lake" {
  name          = "${var.project_name}-data-lake-${var.environment}"
  location      = var.region
  force_destroy = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30  # days
    }
    action {
      type = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}

# Tạo BigQuery Dataset (tương đương với Glue Catalog)
resource "google_bigquery_dataset" "data_catalog" {
  dataset_id  = replace("${var.project_name}_${var.environment}", "-", "_")
  description = "Dataset for data lake catalog"
  location    = var.region

  labels = {
    environment = var.environment
    project     = var.project_name
  }
}

# Tạo BigQuery Table
resource "google_bigquery_table" "sales_data" {
  dataset_id = google_bigquery_dataset.data_catalog.dataset_id
  table_id   = "raw_sales_data"

  time_partitioning {
    type = "DAY"
    field = "transaction_date"
  }

  schema = <<EOF
[
  {
    "name": "transaction_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "customer_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "amount",
    "type": "FLOAT",
    "mode": "REQUIRED"
  },
  {
    "name": "transaction_date",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  }
]
EOF
}