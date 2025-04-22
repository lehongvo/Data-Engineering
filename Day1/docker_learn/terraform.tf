terraform {
required_providers {
google = {
source = "hashicorp/google"
version = "4.51.0"
}
}
}

provider "google" {
project = var.project_id
region = var.region
}

variable "project_id" {
description = "Google Cloud Project ID"
type = string
}

variable "region" {
description = "Region for GCP resources"
default = "asia-southeast1"
type = string
}

resource "google_sql_database_instance" "instance" {
name = "flask-postgres"
database_version = "POSTGRES_13"
region = var.region

settings {
tier = "db-f1-micro"

ip_configuration {
ipv4_enabled = true
authorized_networks {
name = "all"
value = "0.0.0.0/0"
}
}
}

deletion_protection = false
}

resource "google_sql_database" "database" {
name = "postgres"
instance = google_sql_database_instance.instance.name
}

resource "google_sql_user" "users" {
name = "postgres"
instance = google_sql_database_instance.instance.name
password = "postgres"
}

output "database_connection" {
value = "postgresql://postgres:postgres@${google_sql_database_instance.instance.public_ip_address}:5432/postgres"
}
