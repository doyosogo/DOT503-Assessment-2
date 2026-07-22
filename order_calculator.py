"""Business logic for calculating PQS customer order totals."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

MONEY_QUANTIZER = Decimal("0.01")


def _to_decimal(value: Any, field_name: str) -> Decimal:
    """Convert a numeric value to Decimal or raise a clear ValueError."""
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid number.") from exc


def _money(amount: Decimal) -> Decimal:
    """Round a Decimal amount to standard currency precision."""
    return amount.quantize(MONEY_QUANTIZER, rounding=ROUND_HALF_UP)


def validate_items(items: list[dict[str, Any]]) -> None:
    """Validate order item dictionaries before calculation."""
    if not isinstance(items, list):
        raise ValueError("Items must be provided as a list.")

    if not items:
        raise ValueError("At least one item is required.")

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Item {index} must be a dictionary.")

        required_fields = {"name", "price", "quantity"}
        missing_fields = required_fields - item.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Item {index} is missing required field(s): {missing}.")

        if not isinstance(item["name"], str) or not item["name"].strip():
            raise ValueError(f"Item {index} name must be a non-empty string.")

        price = _to_decimal(item["price"], f"Item {index} price")
        if price < 0:
            raise ValueError(f"Item {index} price cannot be negative.")

        quantity = item["quantity"]
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError(f"Item {index} quantity must be a whole number.")

        if quantity <= 0:
            raise ValueError(f"Item {index} quantity must be greater than zero.")


def calculate_subtotal(items: list[dict[str, Any]]) -> Decimal:
    """Calculate the pre-discount order subtotal."""
    validate_items(items)

    subtotal = Decimal("0.00")
    for item in items:
        price = _to_decimal(item["price"], "Item price")
        subtotal += price * item["quantity"]

    return _money(subtotal)


def apply_discount(subtotal: Decimal, discount_percent: Decimal | int | str) -> Decimal:
    """Calculate the discount amount for a subtotal."""
    subtotal = _to_decimal(subtotal, "Subtotal")
    discount = _to_decimal(discount_percent, "Discount percent")

    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative.")

    if discount < 0 or discount > 100:
        raise ValueError("Discount percent must be between 0 and 100.")

    return _money(subtotal * (discount / Decimal("100")))


def calculate_shipping(subtotal: Decimal) -> Decimal:
    """Apply feature-z premium shipping: free at $100.00, $6.50 from $60.00, otherwise $15.00."""
    subtotal = _to_decimal(subtotal, "Subtotal")

    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative.")

    if subtotal >= Decimal("100.00"):
        return Decimal("0.00")

    if subtotal >= Decimal("60.00"):
        return Decimal("6.50")

    return Decimal("15.00")


def calculate_tax(amount: Decimal, tax_rate: Decimal | int | str = Decimal("0.10")) -> Decimal:
    """Calculate tax for a supplied amount."""
    amount = _to_decimal(amount, "Amount")
    tax_rate = _to_decimal(tax_rate, "Tax rate")

    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative.")

    return _money(amount * tax_rate)


def calculate_order_total(
    items: list[dict[str, Any]], discount_percent: Decimal | int | str = 0
) -> dict[str, Decimal]:
    """Calculate subtotal, discount, shipping, tax, and final total."""
    subtotal = calculate_subtotal(items)
    discount = apply_discount(subtotal, discount_percent)
    discounted_subtotal = subtotal - discount
    shipping = calculate_shipping(discounted_subtotal)
    tax = calculate_tax(discounted_subtotal + shipping)
    final_total = _money(discounted_subtotal + shipping + tax)

    return {
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "tax": tax,
        "final_total": final_total,
    }
