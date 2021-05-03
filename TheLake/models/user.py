import datetime
from dbInit import db, FlaskDocument
from passlib.hash import pbkdf2_sha256 as sha256
from mongoengine import StringField

class User(FlaskDocument):
    # pylint: disable=no-member
    email = db.StringField(max_length=255, unique=True)
    firstname = db.StringField(max_length=255)
    lastname = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    isAdmin = db.BooleanField(default=True)

    @staticmethod
    def generateHash(password):
        return sha256.hash(password)

    @staticmethod
    def verifyHash(password, hash):
        return sha256.verify(password, hash)