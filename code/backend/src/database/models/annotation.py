from database import FlaskDocument, database as db


class Annotation(FlaskDocument):
    workspace_id = db.StringField(max_length=255, required=True)
    file_name = db.StringField(max_length=255, requiered=True)
    data_attribute = db.StringField(max_length=255, requiered=True)
    ontology_attribute = db.StringField(max_length=255, requiered=True)
    comment = db.StringField(max_length=255)
