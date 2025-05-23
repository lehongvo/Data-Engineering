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

# VPC Network
resource "google_compute_network" "vpc_network" {
  name                    = "${var.project_name}-${var.environment}-vpc"
  auto_create_subnetworks = false
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_name}-${var.environment}-subnet"
  ip_cidr_range = var.subnet_cidr
  network       = google_compute_network.vpc_network.id
  region        = var.region
}

# Cloud Storage bucket
resource "google_storage_bucket" "data_lake" {
  name          = "${var.project_name}-data-lake-${var.environment}"
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

# BigQuery Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id    = "${replace(var.project_name, "-", "_")}_${var.environment}"
  friendly_name = "Data Engineering Dataset"
  description   = "Dataset for data engineering practice"
  location      = var.region
}

# BigQuery Table
resource "google_bigquery_table" "raw_sales_data" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "raw_sales_data"
  deletion_protection = false
  time_partitioning {
    type  = "DAY"
    field = "transaction_date"
  }

  schema = <<EOF
[
  {
    "name": "transaction_id",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "Unique identifier for the transaction"
  },
  {
    "name": "customer_id",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "Unique identifier for the customer"
  },
  {
    "name": "amount",
    "type": "FLOAT",
    "mode": "REQUIRED",
    "description": "Transaction amount"
  },
  {
    "name": "transaction_date",
    "type": "TIMESTAMP",
    "mode": "REQUIRED",
    "description": "Date and time of the transaction"
  }
]
EOF
}

# Compute Engine Instance
resource "google_compute_instance" "vm_instance" {
  name         = "${var.project_name}-${var.environment}-${var.instance_name}"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.name
    subnetwork = google_compute_subnetwork.subnet.name

    access_config {
      # Ephemeral public IP
    }
  }

  tags = var.instance_tags

  metadata = {
    ssh-keys = "debian:${file("~/.ssh/id_rsa.pub")}"
  }

  metadata_startup_script = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y python3-pip
              pip3 install google-cloud-storage google-cloud-bigquery pandas
              EOF
}
