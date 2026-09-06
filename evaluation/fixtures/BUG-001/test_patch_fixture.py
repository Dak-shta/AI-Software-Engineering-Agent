from patch_fixture import User

def test_email_is_stored():
    user = User("Alice", "alice@example.com")
    assert user.email == "alice@example.com"