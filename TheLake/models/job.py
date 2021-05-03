import datetime

from mongoengine.fields import BooleanField
from dbInit import db, FlaskDocument
from passlib.hash import pbkdf2_sha256 as sha256
from mongoengine import StringField
from models.user import User

class Job(FlaskDocument):
    # pylint: disable=no-member
    uid = db.UUIDField(binary=False, required=True, unique=True)
    task = db.StringField(max_length=255)
    failed = db.BooleanField(default=False)
    errorMessage = db.StringField()
    startedBy = db.LazyReferenceField("User", required=True)
    startedAt = db.DateTimeField()
    endedAt = db.DateTimeField()
    
    meta = {'indexes': [
        {'fields': ['$uid', '$task', '$errorMessage', '$startedBy', '$startedAt', 
        '$endedAt',]
        }
    ]}