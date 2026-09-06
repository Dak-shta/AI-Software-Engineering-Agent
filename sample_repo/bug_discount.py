def calculate_discount(price, is_member):
    if is_member:
        # Apply a 10% discount for members
        return price * 0.9
    return price