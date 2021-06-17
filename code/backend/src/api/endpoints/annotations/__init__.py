from flask_restful import Resource
from flask_restful.reqparse import Argument

from api.services.decorators import parse_params
from database.data_access import annotation_data_access


class Annotation(Resource):

    @parse_params(
        Argument('workspace_id', type=str),
        Argument('file_name', type=str),
        Argument('data_attribute', type=str),
        Argument('ontology_attribute', type=str),
    )
    def post(self, workspace_id, file_name, data_attribute, ontology_attribute):
        # add Annotation
        annotation_data_access.add(workspace_id, file_name, data_attribute, ontology_attribute)
