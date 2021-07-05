from flask import Blueprint
from flask_restful import Api

from api.endpoints.workspaces import Workspaces

WORKSPACE_BLUEPRINT = Blueprint("workspace.py", __name__)

routes = ["/workspaces", "/workspaces/<workspace_id>"]
Api(WORKSPACE_BLUEPRINT).add_resource(Workspaces, *routes)
