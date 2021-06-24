from flask_restful import Resource
from flask_restful.reqparse import Argument

from api.services.decorators import parse_params
from database.data_access import annotation_data_access
from business_logic.services.mapper import mapper


class Annotation(Resource):
    def check_datamart(self, workspace_id, datamart_id):
        """
        Check if file exists in ontology
        :param workspace_id:
        :param datamart_id:
        :return:
        """
        pass

    def check_data_attribute(self, workspace_id, datamart_id, data_attribute):
        """

        :param workspace_id:
        :param datamart_id:
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
        Argument('datamart_id', required=True, type=str),
        Argument('data_attribute', required=True, type=str)
    )
    def get(self, workspace_id, datamart_id, data_attribute=''):
        # API function for accessing annotations of specific attribute
        return mapper(annotation_data_access.get(workspace_id, datamart_id, data_attribute))

    @parse_params(
        Argument('workspace_id', required=True, type=str),
        Argument('datamart_id', required=True, type=str),
        Argument('data_attribute', required=True, type=str),
        Argument('property_description', required=True, type=str),
        Argument('ontology_attribute', required=True, type=str),
        Argument('comment', required=True, type=str)
    )
    def post(self, workspace_id, datamart_id, data_attribute, property_description, ontology_attribute, comment):
        # API function for adding a new annotation
        # ontology_attribute = [value for value in ontology_attribute.values()]
        # print(ontology_attribute)

        return annotation_data_access.add(workspace_id, datamart_id, data_attribute, property_description,
                                          ontology_attribute, comment)

    @parse_params(
        Argument('workspace_id', type=str, required=True),
        Argument('datamart_id', type=str, required=True),
        Argument('data_attribute', type=str, required=True),
        Argument('property_description', type=str, required=True),
        Argument('ontology_attribute', type=str, required=True)
    )
    def delete(self, workspace_id, datamart_id, data_attribute, property_description, ontology_attribute):
        return annotation_data_access.delete(workspace_id, datamart_id, data_attribute, property_description,
                                             ontology_attribute)
