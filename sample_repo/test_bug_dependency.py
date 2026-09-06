from bug_dependency import get_user_email


def test_get_user_email():
    assert get_user_email(
        "Alice",
        "alice@example.com"
    ) == "alice@example.com"