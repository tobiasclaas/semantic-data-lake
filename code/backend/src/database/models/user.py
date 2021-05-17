from database import database, FlaskDocument


class User(FlaskDocument):
    email = database.StringField(max_length=255, unique=True)
    firstname = database.StringField(max_length=255)
    lastname = database.StringField(max_length=255)
    password_hash = database.StringField(max_length=255)
    is_admin = database.BooleanField(default=True)
