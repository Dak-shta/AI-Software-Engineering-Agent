from bug_failure import divide


def test_divide():
    assert divide(10, 2) == 5


def test_zero_division():
    assert divide(10, 0) == 0