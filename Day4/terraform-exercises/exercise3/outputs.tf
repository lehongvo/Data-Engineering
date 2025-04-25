output "bucket_name" {
  description = "The name of the bucket"
  value       = google_storage_bucket.data_lake_bucket.name
}

output "bucket_url" {
  description = "The URL of the bucket"
  value       = google_storage_bucket.data_lake_bucket.url
}

output "dataset_id" {
  description = "The ID of the BigQuery dataset"
  value       = google_bigquery_dataset.data_lake_dataset.dataset_id
}

output "service_account_email" {
  description = "The email of the service account"
  value       = google_service_account.data_lake_sa.email
}

output "service_account_key" {
  description = "The key of the service account in JSON format"
  value       = base64decode(google_service_account_key.data_lake_key.private_key)
  sensitive   = true
}
