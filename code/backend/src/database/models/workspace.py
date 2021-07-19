from database import database, FlaskDocument
from database.models import User
from mongoengine import CASCADE


class Workspace(FlaskDocument):
    name = database.StringField(max_length=255, required=True)
    user = database.ReferenceField(User, reverse_delete_rule=CASCADE)
