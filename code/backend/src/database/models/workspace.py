from database import database, FlaskDocument

class Workspace(FlaskDocument):
    name = database.StringField(max_length=255)
