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

# VPC Network cho Dataflow
resource "google_compute_network" "dataflow_network" {
  name                    = "dataflow-network"
  auto_create_subnetworks = false
}

# Subnet cho Dataflow
resource "google_compute_subnetwork" "dataflow_subnet" {
  name          = "dataflow-subnet"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.dataflow_network.id
  region        = var.region
}

# Cloud Storage buckets
resource "google_storage_bucket" "data_lake" {
  name          = "${var.project_id}-data-lake"
  location      = var.region
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}

resource "google_storage_bucket" "temp_files" {
  name          = "${var.project_id}-temp-files"
  location      = var.region
  force_destroy = true
}

# BigQuery Dataset
resource "google_bigquery_dataset" "analytical_dataset" {
  dataset_id    = "analytical_dataset"
  friendly_name = "Analytical Dataset"
  description   = "Dataset for analytical data"
  location      = var.region

  labels = {
    env = "dev"
  }
}

# Pub/Sub Topic cho streaming data
resource "google_pubsub_topic" "incoming_data" {
  name = "incoming-data"
}

# Service Account cho Dataflow
resource "google_service_account" "dataflow_service_account" {
  account_id   = "dataflow-sa"
  display_name = "Dataflow Service Account"
}