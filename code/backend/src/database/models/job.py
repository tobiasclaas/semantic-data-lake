import datetime
from enum import Enum

from database import database as db

from mongoengine.document import Document
from mongoengine.fields import EnumField


class JobStatus(Enum):
    waiting = 'waiting'
    running = 'running'
    finished = 'finished'
    error = 'error'


class Job(Document):
    status = EnumField(JobStatus, default=JobStatus.waiting)
    submit_time = db.DateTimeField(default=datetime.datetime.now())
    job_name = db.StringField(max_length=255)
