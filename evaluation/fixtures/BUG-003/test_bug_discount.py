from bug_discount import calculate_discount

def test_member_discount():
    assert calculate_discount(100, True) == 90

def test_non_member_price():
    assert calculate_discount(100, False) == 100