TAX_RATE = 0.1  # 10% tax rate


def calculate_tax(amount: float) -> float:
    """Calculate tax for a given amount"""
    return amount * (1 + TAX_RATE)


def apply_discount(amount: float, discount_percent: float) -> float:
    """Apply a percentage discount to an amount"""
    return amount * (1 - discount_percent / 100)


if __name__ == "__main__":
    # This code only runs when utils.py is executed directly
    amount = 100
    print(f"Amount with tax: ${calculate_tax(amount):.2f}")
    print(f"Amount with 20% discount: ${apply_discount(amount, 20):.2f}")
