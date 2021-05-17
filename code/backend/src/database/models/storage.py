from mongoengine.document import EmbeddedDocument

from database import database as db


DATATYPE = ("mongodb", "postgresql", "csv", "json", "xml")


class BaseStorage(EmbeddedDocument):
    datatype = db.StringField(choices=DATATYPE)

    meta = {
        "allow_inheritance": True
    }


class MongodbStorage(BaseStorage):
    datatype = "mongodb"
    host = db.StringField()
    port = db.IntField()
    user = db.StringField()
    password = db.StringField()
    database = db.StringField()
    collection = db.StringField()


class PostgresqlStorage(BaseStorage):
    datatype = "postgresql"
    host = db.StringField()
    port = db.IntField()
    user = db.StringField()
    password = db.StringField()
    database = db.StringField()
    table = db.StringField()


class CsvStorage(BaseStorage):
    datatype = "csv"
    mimetype = "text/csv"
    file = db.StringField()
    has_header = db.BooleanField()
    delimiter = db.StringField()


class JsonStorage(BaseStorage):
    datatype = "json"
    mimetype = "application/json"
    file = db.StringField()


class XmlStorage(BaseStorage):
    datatype = "xml"
    mimetype = "application/xml"
    file = db.StringField()
    row_tag = db.StringField()
