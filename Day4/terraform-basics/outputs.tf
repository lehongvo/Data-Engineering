output "vpc_id" {
  description = "ID của VPC network"
  value       = google_compute_network.vpc.id
}

output "subnet_id" {
  description = "ID của subnet"
  value       = google_compute_subnetwork.subnet.id
}

output "storage_bucket_name" {
  description = "Tên của Cloud Storage bucket (data lake)"
  value       = google_storage_bucket.data_lake.name
}

output "bigquery_dataset_id" {
  description = "ID của BigQuery dataset"
  value       = google_bigquery_dataset.data_catalog.dataset_id
}

output "bigquery_table_id" {
  description = "ID của BigQuery table"
  value       = "${google_bigquery_dataset.data_catalog.dataset_id}.${google_bigquery_table.sales_data.table_id}"
}