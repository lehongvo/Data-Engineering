# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

  # Sandbox configuration
  subscription_id            = "16982123-2d3c-44ce-ab2d-0c419f4ce699"
  skip_provider_registration = true
}

# Create a resource group
resource "azurerm_resource_group" "sandbox" {
  name     = "sandbox-resources"
  location = "East US"
}

# Create Virtual Network
resource "azurerm_virtual_network" "sandbox" {
  name                = "sandbox-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.sandbox.location
  resource_group_name = azurerm_resource_group.sandbox.name
}

# Create Subnet
resource "azurerm_subnet" "sandbox" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.sandbox.name
  virtual_network_name = azurerm_virtual_network.sandbox.name
  address_prefixes     = ["10.0.2.0/24"]
}

# Create Public IP
resource "azurerm_public_ip" "sandbox" {
  name                = "sandbox-public-ip"
  resource_group_name = azurerm_resource_group.sandbox.name
  location            = azurerm_resource_group.sandbox.location
  allocation_method   = "Dynamic"
}

# Create Network Interface
resource "azurerm_network_interface" "sandbox" {
  name                = "sandbox-nic"
  location            = azurerm_resource_group.sandbox.location
  resource_group_name = azurerm_resource_group.sandbox.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.sandbox.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.sandbox.id
  }
}

# Create Linux Virtual Machine
resource "azurerm_linux_virtual_machine" "sandbox" {
  name                = "sandbox-vm"
  resource_group_name = azurerm_resource_group.sandbox.name
  location            = azurerm_resource_group.sandbox.location
  size                = "Standard_B1s" # Smallest size for sandbox
  admin_username      = "azureuser"

  network_interface_ids = [
    azurerm_network_interface.sandbox.id,
  ]

  # Use password authentication for sandbox (not recommended for production)
  admin_password                  = "Password123!"
  disable_password_authentication = false

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
