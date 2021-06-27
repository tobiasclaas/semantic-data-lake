import mongoengine
from database import database, FlaskDocument
from database.models import Workspace

class Dataset(FlaskDocument):
    name = database.StringField(max_length=255)
    type = database.StringField(max_length=255)
    workspace = database.ReferenceField(Workspace, reverse_delete_rule=mongoengine.DENY)
