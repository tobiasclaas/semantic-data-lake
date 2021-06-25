import mongoengine

from database import FlaskDocument, database as db
from database.models import Datamart


class Annotation(FlaskDocument):
    datamart_id = db.ReferenceField(Datamart, reverse_delete_rule=mongoengine.CASCADE)
    data_attribute = db.StringField(max_length=255, requiered=True)
    ontology_attribute = db.ListField(requiered=True)
    comment = db.StringField(max_length=255)
