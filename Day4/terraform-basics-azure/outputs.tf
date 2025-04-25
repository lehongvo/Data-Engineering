output "resource_group_id" {
  description = "Resource Group ID"
  value       = azurerm_resource_group.sandbox.id
}

output "resource_group_location" {
  description = "Resource Group Location"
  value       = azurerm_resource_group.sandbox.location
}

output "public_ip" {
  description = "Public IP Address"
  value       = azurerm_public_ip.sandbox.ip_address
}
