from flask_mongoengine import MongoEngine

database = MongoEngine()


class FlaskDocument(database.Document):
    meta = {
        'abstract': True,
    }

    @classmethod
    def all_subclasses(cls):
        return cls.__subclasses__() + [
            g for s in cls.__subclasses__() for g in s.all_subclasses()
        ]
