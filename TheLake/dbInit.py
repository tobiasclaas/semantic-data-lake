from flask_mongoengine import MongoEngine

db = MongoEngine()


class FlaskDocument(db.Document):
  meta = {
      'abstract': True,
  }

  @classmethod
  def all_subclasses(cls):
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in s.all_subclasses()
    ]
