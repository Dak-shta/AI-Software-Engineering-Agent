from sample_repo.pr_test_change import calculate_total


def test_calculate_total():
    assert calculate_total(10, 3) == 30