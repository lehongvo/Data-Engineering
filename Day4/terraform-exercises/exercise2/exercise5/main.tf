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

# Tạo Cloud Storage bucket cho data lake
resource "google_storage_bucket" "raw_data" {
  name          = "${var.project_id}-raw-data"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
  
  lifecycle_rule {
    condition {
      age = 90  # Chuyển data sau 90 ngày
    }
    action {
      type = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }
}

# Tạo BigQuery Dataset
resource "google_bigquery_dataset" "analytics" {
  dataset_id  = "analytics_raw"
  description = "Dataset for raw data analysis"
  location    = var.region

  default_table_expiration_ms = 7776000000  # 90 days

  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
  
  access {
    role          = "READER"
    special_group = "projectReaders"
  }
}