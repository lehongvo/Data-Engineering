output "vpc_network" {
  description = "The VPC network"
  value       = google_compute_network.vpc_network.name
}

output "vpc_subnet" {
  description = "The VPC subnet"
  value       = google_compute_subnetwork.vpc_subnet.name
}

output "vpc_connector" {
  description = "The VPC connector"
  value       = google_vpc_access_connector.connector.name
}

output "data_lake_bucket" {
  description = "The data lake bucket"
  value       = google_storage_bucket.data_lake.name
}

output "temp_bucket" {
  description = "The temporary storage bucket"
  value       = google_storage_bucket.temp_bucket.name
}

output "pubsub_topic" {
  description = "The Pub/Sub topic"
  value       = google_pubsub_topic.pipeline_topic.name
}

output "pubsub_subscription" {
  description = "The Pub/Sub subscription"
  value       = google_pubsub_subscription.pipeline_subscription.name
}

output "service_account_email" {
  description = "The service account email"
  value       = google_service_account.pipeline_sa.email
}

output "service_account_key" {
  description = "The service account key (base64 encoded)"
  value       = google_service_account_key.pipeline_sa_key.private_key
  sensitive   = true
}
