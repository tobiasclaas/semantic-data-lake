from flask import Blueprint
from flask_restful import Api

from api.endpoints.fuseki import FusekiQuery, FusekiCreateDatabase, FusekiIngestion

FUSEKI_BLUEPRINT = Blueprint("fuseki.py", __name__)

fuseki_routes = ["/fuseki", "/fuseki/query"]
Api(FUSEKI_BLUEPRINT).add_resource(FusekiQuery, *fuseki_routes)

fuseki_routes = ["/fuseki", "/fuseki/create"]
Api(FUSEKI_BLUEPRINT).add_resource(FusekiCreateDatabase, *fuseki_routes)

fuseki_routes = ["/fuseki", "/fuseki/ingest"]
Api(FUSEKI_BLUEPRINT).add_resource(FusekiIngestion, *fuseki_routes)

