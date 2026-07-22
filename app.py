"""Command-line entry point for the PQS Order Calculator."""

from decimal import Decimal

from order_calculator import calculate_order_total


def main() -> None:
    """Run a sample order and print the calculated totals."""
    sample_items = [
        {"name": "PQS Widget", "price": Decimal("19.99"), "quantity": 2},
        {"name": "PQS Cable", "price": Decimal("7.50"), "quantity": 3},
        {"name": "PQS Adapter", "price": Decimal("12.00"), "quantity": 1},
    ]

    result = calculate_order_total(sample_items, discount_percent=10)

    print("PQS Order Calculator")
    print(f"Subtotal: ${result['subtotal']}")
    print(f"Discount: ${result['discount']}")
    print(f"Shipping: ${result['shipping']}")
    print(f"Tax: ${result['tax']}")
    print(f"Final total: ${result['final_total']}")


if __name__ == "__main__":
    main()
