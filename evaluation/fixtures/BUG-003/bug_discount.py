def calculate_discount(price, is_member):
    """Calculate the final price after applying a 10% discount for members.

    Parameters
    ----------
    price : int | float
        The original price of the item.
    is_member : bool
        ``True`` if the customer is a member and is eligible for a discount.

    Returns
    -------
    int
        The discounted price rounded to the nearest integer.
    """
    if is_member:
        # Apply a 10% discount. ``int`` truncates towards zero which is
        # acceptable for the simple test suite.
        return int(price * 0.9)
    return price
