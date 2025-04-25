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

# Create a new storage bucket for data lake
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "${var.project_name}-${var.environment}-lake"
  location      = var.bucket_location
  storage_class = var.storage_class
  force_destroy = true

  # Enable versioning
  versioning {
    enabled = true
  }

  # Enable uniform bucket-level access
  uniform_bucket_level_access = true

  # Public access prevention
  public_access_prevention = "enforced"

  # Object lifecycle management
  dynamic "lifecycle_rule" {
    for_each = var.lifecycle_rules
    content {
      action {
        type          = lifecycle_rule.value.action.type
        storage_class = lifecycle_rule.value.action.storage_class
      }
      condition {
        age                   = lifecycle_rule.value.condition.age
        created_before        = lifecycle_rule.value.condition.created_before
        with_state            = lifecycle_rule.value.condition.with_state
        matches_storage_class = lifecycle_rule.value.condition.matches_storage_class
      }
    }
  }
}

# Create a BigQuery dataset
resource "google_bigquery_dataset" "data_lake_dataset" {
  dataset_id                 = replace("${var.project_name}_${var.environment}_dataset", "-", "_")
  friendly_name              = "${var.project_name} ${var.environment} Dataset"
  description                = "Dataset for ${var.project_name} data lake"
  location                   = var.dataset_location
  delete_contents_on_destroy = true

  # Set default table expiration to 90 days
  default_table_expiration_ms = 7776000000

  # Set access control
  access {
    role          = "OWNER"
    user_by_email = "lehongvi19x@gmail.com"
  }

  access {
    role          = "READER"
    special_group = "projectReaders"
  }

  access {
    role          = "WRITER"
    special_group = "projectWriters"
  }
}

# Create a service account for data lake access
resource "google_service_account" "data_lake_sa" {
  account_id   = "${var.project_name}-${var.environment}-sa"
  display_name = "Service Account for ${var.project_name} data lake access"
}

# Create custom role for data lake access
resource "google_project_iam_custom_role" "data_lake_role" {
  role_id     = replace("${var.project_name}_${var.environment}_lake_role", "-", "_")
  title       = "${var.project_name} ${var.environment} Lake Role"
  description = "Custom role for data lake access"
  permissions = [
    "storage.buckets.get",
    "storage.buckets.getIamPolicy",
    "storage.buckets.setIamPolicy",
    "storage.objects.create",
    "storage.objects.delete",
    "storage.objects.get",
    "storage.objects.list",
    "storage.objects.update",
    "bigquery.datasets.get",
    "bigquery.tables.get",
    "bigquery.tables.getData",
    "bigquery.tables.list",
    "bigquery.tables.update",
    "bigquery.tables.updateData"
  ]
}

# Create a key for the service account
resource "google_service_account_key" "data_lake_key" {
  service_account_id = google_service_account.data_lake_sa.name
  depends_on         = [google_service_account.data_lake_sa]
}

# Grant admin permissions to the user first
resource "google_storage_bucket_iam_member" "user_admin" {
  bucket     = google_storage_bucket.data_lake_bucket.name
  role       = "roles/storage.admin"
  member     = "user:lehongvi19x@gmail.com"
  depends_on = [google_storage_bucket.data_lake_bucket]
}

# Grant the custom role to the service account
resource "google_project_iam_member" "custom_role_binding" {
  project = var.project_id
  role    = "projects/${var.project_id}/roles/${google_project_iam_custom_role.data_lake_role.role_id}"
  member  = "serviceAccount:${google_service_account.data_lake_sa.email}"
  depends_on = [
    google_service_account.data_lake_sa,
    google_project_iam_custom_role.data_lake_role,
    google_storage_bucket_iam_member.user_admin
  ]
}

# Grant BigQuery permissions to the service account
resource "google_bigquery_dataset_iam_member" "dataset_user" {
  dataset_id = google_bigquery_dataset.data_lake_dataset.dataset_id
  role       = "roles/bigquery.dataViewer"
  member     = "serviceAccount:${google_service_account.data_lake_sa.email}"
  depends_on = [google_bigquery_dataset.data_lake_dataset, google_service_account.data_lake_sa]
}

# Grant storage permissions to the service account
resource "google_storage_bucket_iam_binding" "bucket_viewer" {
  bucket = google_storage_bucket.data_lake_bucket.name
  role   = "roles/storage.objectViewer"
  members = [
    "serviceAccount:${google_service_account.data_lake_sa.email}",
    "user:lehongvi19x@gmail.com"
  ]
  depends_on = [
    google_storage_bucket.data_lake_bucket,
    google_service_account.data_lake_sa,
    google_storage_bucket_iam_member.user_admin
  ]
}

resource "google_storage_bucket_iam_binding" "bucket_creator" {
  bucket = google_storage_bucket.data_lake_bucket.name
  role   = "roles/storage.objectCreator"
  members = [
    "serviceAccount:${google_service_account.data_lake_sa.email}",
    "user:lehongvi19x@gmail.com"
  ]
  depends_on = [
    google_storage_bucket.data_lake_bucket,
    google_service_account.data_lake_sa,
    google_storage_bucket_iam_member.user_admin,
    google_storage_bucket_iam_binding.bucket_viewer
  ]
}
