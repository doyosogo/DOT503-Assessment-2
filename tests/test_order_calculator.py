"""Unit tests for the PQS Order Calculator assessment."""

from decimal import Decimal

from order_calculator import (
    apply_discount,
    calculate_shipping,
    calculate_subtotal,
    calculate_tax,
)


def test_calculate_subtotal_multiple_items() -> None:
    """Subtotal should include each item price multiplied by quantity."""
    items = [
        {"name": "PQS Widget", "price": Decimal("19.99"), "quantity": 2},
        {"name": "PQS Cable", "price": Decimal("7.50"), "quantity": 3},
        {"name": "PQS Adapter", "price": Decimal("12.00"), "quantity": 1},
    ]

    assert calculate_subtotal(items) == Decimal("74.48")


def test_apply_discount_calculates_percentage_discount() -> None:
    """Discount should calculate the percentage amount from the subtotal."""
    assert apply_discount(Decimal("200.00"), 15) == Decimal("30.00")


def test_calculate_shipping_applies_current_premium_middle_tier() -> None:
    """Premium shipping should be $6.50 from $60.00 to $99.99."""
    assert calculate_shipping(Decimal("74.48")) == Decimal("6.50")


def test_calculate_shipping_outdated_expectation_fails() -> None:
    """Deliberately fail by expecting an outdated shipping amount."""
    # Assessment demonstration: automated testing detects this incorrect expectation.
    assert calculate_shipping(Decimal("74.48")) == Decimal("8.95")


def test_calculate_tax_incorrect_expectation_fails() -> None:
    """Deliberately fail by expecting an incorrect tax value."""
    # Assessment demonstration: automated testing detects this incorrect expectation.
    assert calculate_tax(Decimal("100.00")) == Decimal("9.50")
