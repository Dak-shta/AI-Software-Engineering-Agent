from sample_repo.refactoring_example import (
    calculate_order_total,
    calculate_order_total_with_discount,
)


def test_calculate_order_total():
    items = [
        {"price": 10, "quantity": 2},
        {"price": 5, "quantity": 3},
    ]

    assert calculate_order_total(items) == 35


def test_calculate_order_total_with_zero_quantity():
    items = [
        {"price": 10, "quantity": 0},
        {"price": 5, "quantity": 3},
    ]

    assert calculate_order_total(items) == 15


def test_calculate_order_total_with_discount():
    items = [
        {"price": 10, "quantity": 2},
        {"price": 5, "quantity": 3},
    ]

    assert calculate_order_total_with_discount(items, 0.1) == 31.5


def test_discount_zero():
    items = [
        {"price": 10, "quantity": 2},
    ]

    assert calculate_order_total_with_discount(items, 0) == 20