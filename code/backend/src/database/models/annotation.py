from database import FlaskDocument, database as db
#    meta = {
#        "indexes": [{
#            "fields": [
#                "$uid"
#            ],
#            "sparse": True,
#            "unique": False
#        }]
#    }


class Annotation(FlaskDocument):
    workspace_id = db.UUIDField(binary=False, requiered=True)  # of workspace
    file_name = db.StringField(binary=False, requiered=True)
    data_attribute = db.StringField(max_length=255)
    ontology_attribute = db.StringField(max_length=255)
    comment = db.StringField(max_length=255)

#    meta = {
#        "indexes": [{
#            "fields": [
#                "$uid"
#            ],
#            "sparse": True,
#            "unique": False
#        }]
#    }
