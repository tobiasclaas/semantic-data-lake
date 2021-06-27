from flask_restful import Resource
from flask_restful.reqparse import Argument

from api.services.decorators import parse_params
from database.data_access import annotation_data_access
from business_logic.services.mapper import mapper


class Annotation(Resource):
    @parse_params(
        Argument('datamart_id', required=True, type=str),
        Argument('data_attribute', required=True, type=str)
    )
    def get(self, datamart_id, data_attribute=''):
        # API function for accessing annotations of specific attribute
        return mapper(annotation_data_access.get(datamart_id, data_attribute))

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
        Argument('datamart_id', type=str, required=True),
        Argument('data_attribute', type=str, required=True),
        Argument('property_description', type=str, required=True),
        Argument('ontology_attribute', type=str, required=True)
    )
    def delete(self, datamart_id, data_attribute, property_description, ontology_attribute):
        return annotation_data_access.delete(datamart_id, data_attribute, property_description,
                                             ontology_attribute)
