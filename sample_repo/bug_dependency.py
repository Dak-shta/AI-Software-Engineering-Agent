from models import User


def get_user_email(name, email):
    user = User(name, email)
    return user.email