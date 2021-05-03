import datetime

from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField
from dbInit import db, FlaskDocument
from passlib.hash import pbkdf2_sha256 as sha256
from mongoengine import StringField
from models.user import User


class Ancestor(EmbeddedDocument):
    uid = db.StringField()
    heritage = db.ListField(EmbeddedDocumentField("Ancestor"))


'''Strukturelle Metadaten: Schlüssel extrahieren'''
class MetaData(FlaskDocument):
    # pylint: disable=no-member
    # genral
    comment = db.StringField(max_length=255) #kurzbeschreibung durch user
    heritage = db.ListField(EmbeddedDocumentField(Ancestor))
    humanReadableName = db.StringField(max_length=255)
    insertedAt = db.DateTimeField()
    insertedBy = db.LazyReferenceField("User", required=True)
    isDatabase = db.BooleanField(default=False)
    schema = db.StringField()
    targetStorageSystem = db.StringField(max_length=255)
    targetURL = db.StringField(max_length=255)
    uid = db.UUIDField(binary=False, required=True, unique=True)
    # if source is database
    sourceConnection = db.StringField(max_length=255)
    sourceUser = db.StringField(max_length=255)
    sourcePassword = db.StringField(max_length=255)
    sourceDBName = db.StringField(max_length=255)
    sourceCollectionOrTableName = db.StringField(max_length=255)
    # if target is file
    csvHasHeader = db.BooleanField(default=False)
    csvDelimiter = db.StringField(max_length=255)
    filename = db.StringField(max_length=255)
    mimetype = db.StringField()
    xmlRowTag = db.StringField(max_length=255)
    # for constructed datamarts
    constructionCode = db.StringField()
    constructionQuery = db.StringField()

    meta = {'indexes': [
        {'fields': ['$uid', '$sourceConnection', '$sourceUser', '$sourcePassword', '$sourceDBName', 
        '$sourceCollectionOrTableName', '$schema', '$insertedAt', '$comment', 
        '$filename', '$insertedBy', '$targetStorageSystem', '$humanReadableName', '$xmlRowTag']
        }
    ]}