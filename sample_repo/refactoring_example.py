def _calculate_items_total(items):
    total = 0

    for item in items:
        price = item["price"]
        quantity = item["quantity"]

        if quantity > 0:
            subtotal = price * quantity
            total = total + subtotal

    return total


def calculate_order_total(items):
    return _calculate_items_total(items)


def calculate_order_total_with_discount(items, discount):
    total = _calculate_items_total(items)

    if discount > 0:
        total = total - (total * discount)

    return total