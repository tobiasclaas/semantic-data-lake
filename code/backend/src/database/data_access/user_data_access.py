from database.models import User
from werkzeug.exceptions import NotFound, Conflict
from passlib.hash import pbkdf2_sha256 as sha256


def get_by_email(email) -> User:
    user: User = User.objects(email__exact=email)

    if not user:
        raise NotFound(f"User with email {email} not found")

    return user.get()


def get_all() -> [User]:
    return User.objects.all()
