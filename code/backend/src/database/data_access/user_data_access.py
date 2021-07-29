from database.models import User
from werkzeug.exceptions import NotFound, Conflict
from passlib.hash import pbkdf2_sha256 as sha256


def get_by_email(email) -> User:
    """
    Helper function to return a user via its associated email string

    :param email: email string
    :returns: all users with the given email.
    """
    user: User = User.objects(email__exact=email)

    if not user:
        raise NotFound(f"User with email {email} not found")

    return user.get()


def get_all() -> [User]:
    """
    Helper function to return all users 

    :returns: all users.
    """
    return User.objects.all()
