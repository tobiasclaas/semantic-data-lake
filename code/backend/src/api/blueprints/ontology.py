from flask import Blueprint
from flask_restful import Api

from api.endpoints.ontologies import Ontologies, OntologiesSearch

ONTOLOGY_BLUEPRINT = Blueprint("ontology.py", __name__)

routesSearch = ["/workspaces/<workspace_id>/ontologies/search"]
Api(ONTOLOGY_BLUEPRINT).add_resource(OntologiesSearch, *routesSearch)

routes = ["/workspaces/<workspace_id>/ontologies", "/workspaces/<workspace_id>/ontologies/<id>"]
Api(ONTOLOGY_BLUEPRINT).add_resource(Ontologies, *routes)

