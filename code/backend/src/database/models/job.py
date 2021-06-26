import datetime
from enum import Enum

from database import database as db

from database import FlaskDocument
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, EnumField


class JobStatus(Enum):
    waiting = 'waiting'
    running = 'running'
    finished = 'finished'
    error = 'error'


class JobTask(EmbeddedDocument):
    operation = db.StringField(required=True)
    mart1 = db.DictField(required=True)
    mart2 = db.DictField()


class Job(Document):
    status = EnumField(JobStatus, default=JobStatus.waiting)
    submit_time = db.DateTimeField(default=datetime.datetime.now())
    jobtasks = db.EmbeddedDocumentListField(JobTask)
