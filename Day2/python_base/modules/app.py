import sys
from ecommerce.shopping.cart import ShoppingCart
from ecommerce.shopping.order import Order
from ecommerce.customer import Customer
import ecommerce.utils as utils

# Module Search Path
print("\n=== Module Search Path ===")
for path in sys.path:
    print(path)

# Creating instances from our modules
print("\n=== Using Our Modules ===")
cart = ShoppingCart()
cart.add_item("Phone", 999.99)
cart.add_item("Headphones", 99.99)
print(f"Cart total: ${cart.get_total():.2f}")

# Using the Customer class
customer = Customer("John Doe", "john@example.com")
print(f"Customer: {customer}")

# Create an order
order = Order(customer, cart)
order.place()

# Using utility functions
print("\n=== Using Utility Functions ===")
price = 100
with_tax = utils.calculate_tax(price)
with_discount = utils.apply_discount(price, 10)
print(f"Original price: ${price}")
print(f"With tax: ${with_tax:.2f}")
print(f"With 10% discount: ${with_discount:.2f}")

# Using dir() function
print("\n=== Dir Function ===")
print("Names in current module:", dir())
print("\nNames in ShoppingCart class:", dir(ShoppingCart))

# Module execution information
print("\n=== Module Information ===")
print(f"Current module name: {__name__}")
print("This will only run if the module is executed directly")
