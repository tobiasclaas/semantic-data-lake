from flask_restful import Resource
from flask_restful.reqparse import Argument

from api.services.decorators import parse_params
from database.data_access import annotation_data_access
from business_logic.services.mapper import mapper


class Annotation(Resource):
    def check_workspace(self, workspace_id):
        """
        Checks if workspace exists.
        :param workspace_id:
        :return:
        """
        pass

    def check_file(self, workspace_id, file_name):
        """
        Check if file exists in ontology
        :param workspace_id:
        :param file_name:
        :return:
        """
        pass

    def check_data_attribute(self, workspace_id, file_name, data_attribute):
        """

        :param workspace_id:
        :param file_name:
        :param data_attribute:
        :return:
        """
        pass

    def check_ontology_attribute(self, workspace_id, ontology_attribute):
        """
        Check if attribute exists in ontology. ?Query default graph?
        :param workspace_id:
        :param ontology_attribute:
        :return:
        """
        pass

    @parse_params(
        Argument('workspace_id', required=True, type=str),
        Argument('file_name', required=True, type=str),
        Argument('data_attribute', required=True, type=str),
        Argument('ontology_attribute', required=True, type=str),
        Argument('comment', required=True, type=str)
    )
    def post(self, workspace_id, file_name, data_attribute, ontology_attribute, comment):
        # API function for adding a new annotation
        return annotation_data_access.add(workspace_id, file_name, data_attribute, ontology_attribute, comment)

    @parse_params(
        Argument('workspace_id', required=True, type=str),
        Argument('file_name', required=True, type=str),
        Argument('data_attribute', required=True, type=str)
    )
    def get(self, workspace_id, file_name, data_attribute=''):
        # API function for accessing annotations of specific attribute
        return mapper(annotation_data_access.get(workspace_id, file_name, data_attribute))

    @parse_params(
        Argument('workspace_id', type=str, required=True),
        Argument('file_name', type=str, required=True),
        Argument('data_attribute', type=str, required=True),
        Argument('ontology_attribute', type=str)
    )
    def delete(self, workspace_id, file_name, data_attribute, ontology_attribute=''):
        if ontology_attribute != '':
            return annotation_data_access.delete(workspace_id, file_name, data_attribute, ontology_attribute)
        else:
            return annotation_data_access.delete_all(workspace_id, file_name, data_attribute)
