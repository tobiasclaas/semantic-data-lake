from flask import Blueprint
from flask_restful import Api

from api.endpoints.annotations import Annotation

ANNOTATION_BLUEPRINT = Blueprint("annotation.py", __name__)

annotation_routes = ["/annotation"]
Api(ANNOTATION_BLUEPRINT).add_resource(Annotation, *annotation_routes)
