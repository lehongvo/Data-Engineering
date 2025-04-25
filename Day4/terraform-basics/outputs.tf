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

output "instance_name" {
  description = "The name of the VM instance"
  value       = google_compute_instance.vm_instance.name
}

output "instance_external_ip" {
  description = "The external IP of the VM instance"
  value       = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
}

output "instance_internal_ip" {
  description = "The internal IP of the VM instance"
  value       = google_compute_instance.vm_instance.network_interface[0].network_ip
}
