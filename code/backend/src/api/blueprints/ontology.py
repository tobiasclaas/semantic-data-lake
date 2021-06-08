from flask import Blueprint
from flask_restful import Api

from api.endpoints.ontologies import Ontologies

ONTOLOGY_BLUEPRINT = Blueprint("ontology.py", __name__)

routes = ["/workspaces/<workspace_id>/ontologies", "/workspaces/<workspace_id>/ontologies/<id>"]
Api(ONTOLOGY_BLUEPRINT).add_resource(Ontologies, *routes)
