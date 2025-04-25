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

# Create VPC Network
resource "google_compute_network" "vpc_network" {
  name                    = "${var.vpc_network_name}-${var.environment}"
  auto_create_subnetworks = false
}

# Create VPC Subnet
resource "google_compute_subnetwork" "vpc_subnet" {
  name          = "${var.vpc_network_name}-subnet-${var.environment}"
  ip_cidr_range = var.vpc_subnet_cidr
  network       = google_compute_network.vpc_network.id
  region        = var.region

  # Enable private Google access for Dataflow
  private_ip_google_access = true
}

# Create Serverless VPC Access Connector
resource "google_vpc_access_connector" "connector" {
  name          = "vpc-con-${var.environment}"
  ip_cidr_range = var.vpc_connector_range
  network       = google_compute_network.vpc_network.name
  region        = var.region
}

# Create firewall rules
resource "google_compute_firewall" "dataflow_internal" {
  name    = "allow-dataflow-internal-${var.environment}"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["12345-12346"]
  }

  source_tags = ["dataflow"]
  target_tags = ["dataflow"]
}

# Create Cloud Storage buckets
resource "google_storage_bucket" "data_lake" {
  name          = "${var.project_name}-${var.environment}-lake"
  location      = var.bucket_location
  storage_class = var.data_lake_storage_class
  force_destroy = true

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket" "temp_bucket" {
  name          = "${var.project_name}-${var.environment}-temp"
  location      = var.bucket_location
  storage_class = var.temp_storage_class
  force_destroy = true

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }
}

# Create Pub/Sub Topic
resource "google_pubsub_topic" "pipeline_topic" {
  name = "${var.topic_name}-${var.environment}"
}

# Create Pub/Sub Subscription
resource "google_pubsub_subscription" "pipeline_subscription" {
  name  = "${var.subscription_name}-${var.environment}"
  topic = google_pubsub_topic.pipeline_topic.name

  ack_deadline_seconds = 20

  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering = true
}

# Create Service Account
resource "google_service_account" "pipeline_sa" {
  account_id   = "${var.project_name}-${var.environment}-sa"
  display_name = "Service Account for ${var.project_name} pipeline"
}

# Assign roles to Service Account
resource "google_project_iam_member" "sa_roles" {
  for_each = toset(var.service_account_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# Grant Service Account access to buckets
resource "google_storage_bucket_iam_member" "data_lake_access" {
  bucket = google_storage_bucket.data_lake.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

resource "google_storage_bucket_iam_member" "temp_bucket_access" {
  bucket = google_storage_bucket.temp_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# Create a service account key
resource "google_service_account_key" "pipeline_sa_key" {
  service_account_id = google_service_account.pipeline_sa.name
  depends_on         = [google_service_account.pipeline_sa]
}
