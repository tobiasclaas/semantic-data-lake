from flask import Blueprint
from flask_restful import Api

from api.endpoints.fuseki import Fuseki

FUSEKI_BLUEPRINT = Blueprint("fuseki.py", __name__)

fuseki_routes = ["/fuseki"]
Api(FUSEKI_BLUEPRINT).add_resource(Fuseki, *fuseki_routes)
