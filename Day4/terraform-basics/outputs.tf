output "vpc_network_id" {
  description = "The ID of the VPC network"
  value       = google_compute_network.vpc_network.id
}

output "subnet_id" {
  description = "The ID of the subnet"
  value       = google_compute_subnetwork.subnet.id
}

output "data_lake_bucket" {
  description = "The name of the data lake bucket"
  value       = google_storage_bucket.data_lake.name
}

output "bigquery_dataset" {
  description = "The ID of the BigQuery dataset"
  value       = google_bigquery_dataset.dataset.dataset_id
}

output "bigquery_table" {
  description = "The ID of the BigQuery table"
  value       = google_bigquery_table.raw_sales_data.table_id
} 
