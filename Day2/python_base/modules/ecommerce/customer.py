class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __str__(self):
        return f"{self.name} ({self.email})"


if __name__ == "__main__":
    # This code only runs when customer.py is executed directly
    customer = Customer("Test Customer", "test@example.com")
    print(customer)
