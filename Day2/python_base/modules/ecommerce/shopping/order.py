from ..customer import Customer
from .cart import ShoppingCart
from datetime import datetime


class Order:
    def __init__(self, customer: Customer, cart: ShoppingCart):
        self.customer = customer
        self.cart = cart
        self.date = datetime.now()
        self.total = cart.get_total()

    def place(self):
        print(f"\nOrder placed successfully!")
        print(f"Customer: {self.customer.name}")
        print(f"Email: {self.customer.email}")
        print(f"Date: {self.date}")
        print(f"Total: ${self.total:.2f}")
        print("\nItems:")
        for item in self.cart.get_items():
            print(f"- {item['name']}: ${item['price']:.2f}")


if __name__ == "__main__":
    # This code only runs when order.py is executed directly
    customer = Customer("Test User", "test@example.com")
    cart = ShoppingCart()
    cart.add_item("Test Item", 9.99)
    order = Order(customer, cart)
    order.place()
