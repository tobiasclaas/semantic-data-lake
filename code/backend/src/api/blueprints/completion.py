from flask import Blueprint
from flask_restful import Api

from api.endpoints.completion import Completion

COMPLETION_BLUEPRINT = Blueprint("__init__.py", __name__)

completion_routes = ["/completion"]
Api(COMPLETION_BLUEPRINT).add_resource(Completion, *completion_routes)
