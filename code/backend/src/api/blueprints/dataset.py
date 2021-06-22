from flask import Blueprint
from flask_restful import Api

from api.endpoints.datasets import Datasets

DATASET_BLUEPRINT = Blueprint("dataset.py", __name__)

routes = ["/workspaces/<workspace_id>/datasets", "/workspaces/<workspace_id>/datasets/<id>"]
Api(DATASET_BLUEPRINT).add_resource(Datasets, *routes)

