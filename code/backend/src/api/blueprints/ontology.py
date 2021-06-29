from flask import Blueprint
from flask_restful import Api

from api.endpoints.ontologies import Ontologies, OntologiesSearch, Annotation, Completion

ONTOLOGY_BLUEPRINT = Blueprint("ontology.py", __name__)

search_routes = ["/workspaces/<workspace_id>/ontologies/search"]
Api(ONTOLOGY_BLUEPRINT).add_resource(OntologiesSearch, *search_routes)

routes = ["/workspaces/<workspace_id>/ontologies", "/workspaces/<workspace_id>/ontologies/<id>"]
Api(ONTOLOGY_BLUEPRINT).add_resource(Ontologies, *routes)

annotation_routes = ["/workspaces/<workspace_id>/ontologies/annotation"]
Api(ONTOLOGY_BLUEPRINT).add_resource(Annotation, *annotation_routes)

completion_routes = ["/workspaces/<workspace_id>/ontologies/completion"]
Api(ONTOLOGY_BLUEPRINT).add_resource(Completion, *completion_routes)

