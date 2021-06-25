from enum import Enum

from database import FlaskDocument, database as db
from mongoengine.document import EmbeddedDocument
from database.models.metadata import Metadata


class DatamartState(Enum):
    RUNNING = 0
    SUCCESS = 1
    FAILED = 2


class DatamartStatus(EmbeddedDocument):
    state = db.EnumField(DatamartState)
    started = db.DateTimeField()
    ended = db.DateTimeField()
    error = db.StringField()


class Datamart(FlaskDocument):
    uid = db.StringField(primary_key=True, binary=False, required=True)
    workspace_id = db.StringField(max_length=255)
    human_readable_name = db.StringField(max_length=255)
    comment = db.StringField(max_length=255)
    metadata = db.EmbeddedDocumentField(Metadata)
    status = db.EmbeddedDocumentField("DatamartStatus")

    meta = {
        "indexes": [{
            "fields": [
                "$uid",
                "$human_readable_name",
                "$comment",
                "$metadata.created_at",
                "$metadata.created_by.firstname",
                "$metadata.created_by.lastname",
                "$metadata.created_by.email",
                "$metadata.source.datatype",
                "$metadata.target.datatype",
                "$status.state",
                "$status.started",
                "$status.ended",
            ],
            "sparse": True,
            "unique": False
        }]
    }
