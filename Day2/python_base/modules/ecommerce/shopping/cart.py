class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float):
        self.items.append({"name": name, "price": price})

    def remove_item(self, name: str):
        self.items = [item for item in self.items if item["name"] != name]

    def get_total(self) -> float:
        return sum(item["price"] for item in self.items)

    def get_items(self):
        return self.items.copy()


if __name__ == "__main__":
    # This code only runs when cart.py is executed directly
    cart = ShoppingCart()
    cart.add_item("Test Item", 9.99)
    print(f"Cart total: ${cart.get_total():.2f}")
