from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField

from database import database as db


class Metadata(EmbeddedDocument):
    created_at = db.DateTimeField()
    created_by = db.LazyReferenceField("User")
    schema = db.StringField()

    heritage = db.ListField(db.LazyReferenceField("Datamart"))
    construction_code = db.StringField()
    construction_query = db.StringField()

    source = EmbeddedDocumentField("BaseStorage")
    target = EmbeddedDocumentField("BaseStorage")
