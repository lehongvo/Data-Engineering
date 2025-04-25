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
  region  = var.primary_region
}

provider "google" {
  alias   = "dr"
  project = var.project_id
  region  = var.dr_region
}

# Module cho Data Warehouse trong region chính
module "primary_warehouse" {
  source = "./modules/data_warehouse"

  project_id   = var.project_id
  region       = var.primary_region
  environment  = var.environment
  dataset_name = "primary_warehouse"

  tables = {
    sales = {
      schema = file("${path.module}/schemas/sales.json")
      partitioning = {
        field = "date"
        type  = "DAY"
      }
    }
    customers = {
      schema = file("${path.module}/schemas/customers.json")
    }
  }
}

# Module cho Disaster Recovery region
module "dr_warehouse" {
  source = "./modules/data_warehouse"
  providers = {
    google = google.dr
  }

  project_id   = var.project_id
  region       = var.dr_region
  environment  = var.environment
  dataset_name = "dr_warehouse"

  tables = {
    sales = {
      schema = file("${path.module}/schemas/sales.json")
      partitioning = {
        field = "date"
        type  = "DAY"
      }
    }
    customers = {
      schema = file("${path.module}/schemas/customers.json")
    }
  }
}

# Scheduled transfer giữa primary và DR
resource "google_bigquery_data_transfer_config" "warehouse_backup" {
  display_name           = "warehouse-backup"
  location               = var.primary_region
  data_source_id         = "cross_region_copy"
  destination_dataset_id = module.dr_warehouse.dataset_id
  params = {
    source_dataset_id           = module.primary_warehouse.dataset_id
    overwrite_destination_table = true
  }
  schedule = "every 24 hours"
  disabled = false
}
