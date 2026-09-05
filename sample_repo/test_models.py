from models import User


def test_user_creation():
    user = User("Alice")

    assert user.name == "Alice"


def test_user_email():
    user = User(
        "Alice",
        "alice@example.com"
    )

    assert user.email == "alice@example.com"