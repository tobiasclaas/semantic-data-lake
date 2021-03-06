import json
from flask import jsonify, Response
from flask_restful import Resource
from flask_restful.reqparse import Argument
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import FileStorage
from requests import post
from flask_jwt_extended import jwt_required, get_jwt_identity

import settings
from api.services.decorators import parse_params
from utils.services.mapper import mapper
from database.data_access import ontology_data_access, annotation_data_access


class Ontologies(Resource):
    """
    Class for managing ontologies.
    """

    @jwt_required
    def get(self, workspace_id):
        """
        API get request for ontologies.

        :param workspace_id: id of workspace.
        :returns: all ontologies of a given workspace in JSON format.
        """
        return jsonify([mapper(item) for item in ontology_data_access.get_all(workspace_id)])

    @jwt_required
    @parse_params(
        Argument("file", type=FileStorage, location='files', required=False),
        Argument("name", default=None, type=str, required=False)
    )
    def post(self, name, file, workspace_id):
        """
        API post request to add a new ontology.

        :param name: Name of new ontology.
        :param file: The file containing the ontology.
        :param workspace_id: id of workspace the file is to be added.
        :returns: newly added entry in MongoDB in JSON format.
        """
        return jsonify(mapper(ontology_data_access.add(name, file, workspace_id)))

    @jwt_required
    def delete(self, workspace_id, ontology_id):
        """
        API delete request for deleting an ontology from a workspace.

        :param workspace_id: id of workspace.
        :param ontology_id: id of ontology in MongoDB.
        :return: HTTP-Code 200 if the deletion was successful and failure-code otherwise.
        """
        try:
            ontology_data_access.delete(workspace_id, ontology_id)
            return Response(status=200)
        except HTTPException as inst:
            return mapper(Response(status=inst.code))


class OntologiesSearch(Resource):
    """ Provides requests to search or query ontologies in fuseki directly. """

    @jwt_required
    @parse_params(
        Argument("querystring", required=True, type=str),
        Argument("graph_name", default='?g', type=str),
        Argument("is_query", default=False, type=bool)
    )
    def get(self, workspace_id, querystring, graph_name, is_query):
        """
        Get request to query fuseki.

        :param workspace_id: ID of workspace.
        :param querystring: A keyword or the query itself.
        :param graph_name: ID of Graph in Fuseki, not the entire URL.
        :param is_query: A bool value if a query or keyword is given in querystring.
        :return: The results in either triple(subject, predicate, object) format or as described in the user query.
        """
        if is_query:
            # query fuseki with user defined query
            return jsonify(post('http://localhost:3030/' + workspace_id,
                                auth=(settings.Settings().fuseki_storage.user,
                                      settings.Settings().fuseki_storage.password),
                                data={'query': querystring}).content.decode('utf-8'))

        if not (graph_name == '?g'):  # name of graph is adjusted to as is in fuseki
            graph_name = '<http://localhost:3030/' + workspace_id + '/' + graph_name + '>'
        r = post('http://localhost:3030/' + workspace_id, auth=(settings.Settings().fuseki_storage.user,
                                                                settings.Settings().fuseki_storage.password),
                 data={'query': ontology_data_access.create_query_string(graph_name, querystring)})

        return jsonify(r.content.decode('utf-8'))


class Annotation(Resource):
    """ API class to manage Annotations. """

    @jwt_required
    @parse_params(
        Argument('datamart_id', required=True, type=str),
        Argument('data_attribute', type=str, default=None)
    )
    def get(self, workspace_id, datamart_id, data_attribute):
        """
        Get all annotations for a specific data_attribute.

        :param workspace_id: id of workspace that contains datamart with datamart_id. Is not used but part of the url.
        :param datamart_id: id of the datamart.
        :param data_attribute: name of the attribute.
        :return: Annotation objects.
        """
        try:
            ret = annotation_data_access.get(datamart_id, data_attribute)

            if len(ret) == 0:
                return []
            else:
                return jsonify([mapper(i) for i in ret])
        except HTTPException as ex:
            return Response(status=ex.code)

    @jwt_required
    @parse_params(
        Argument('datamart_id', required=True, type=str),
        Argument('data_attribute', required=True, type=str),
        Argument('property_description', required=True, type=str),
        Argument('ontology_attribute', required=True, type=str),
        Argument('comment', default='', type=str)
    )
    def post(self, workspace_id, datamart_id, data_attribute, property_description, ontology_attribute, comment):
        """
        Post method to add new annotations to mongoDB.

        :param workspace_id: id of workspace that contains datamart with datamart_id
        :param datamart_id: id of datamart which contains data_attribute.
        :param data_attribute: name of the column to be annotated.
        :param property_description: a description for the ontology_attribute that the data_attribute is to be
            annotated with.
        :param ontology_attribute: the ontology class that provides semantic meaning for the data_attribute.
        :param comment: A comment, may give some information about the datamart or the status of the annotation or
            ontologies that are used.
        :return: HTTPResponse depending on success or failure of the annotation.
        """
        try:
            ret = annotation_data_access.add(workspace_id, datamart_id, data_attribute, property_description,
                                             ontology_attribute, comment)
            return mapper(ret)
        except HTTPException as ex:
            return Response(status=ex.code)

    @jwt_required
    @parse_params(
        Argument('datamart_id', type=str, required=True),
        Argument('data_attribute', type=str, required=True),
        Argument('ontology_attribute', type=str, required=True)
    )
    def delete(self, workspace_id, datamart_id, data_attribute, ontology_attribute):
        """
        API delete request to delete annotations.

        :param workspace_id: id of workspace that contains datamart with datamart_id. Is not used but part of the url.
        :param datamart_id: id of datamart that contains data_attribute.
        :param data_attribute: name of the column to be annotated.
        :param ontology_attribute: the ontology class that provides semantic meaning for the data_attribute.
        :return:
        """
        try:
            annotation_data_access.delete(datamart_id, data_attribute, ontology_attribute)
            return Response(status=200)
        except HTTPException as ex:
            return Response(status=ex.code)


class Completion(Resource):
    """
    Class for search and suggestion requests.
    """
    @jwt_required
    @parse_params(
        Argument('search_term', required=True, type=str)
    )
    def get(self, workspace_id, search_term=''):
        """
        Get API for auto completion feature.

        :param workspace_id: id of current workspace
        :param search_term: keyword to be auto completed.
        :returns: ontology-attribute with according label or failure http-code
        """
        try:
            ret = json.loads(ontology_data_access.get_suggestions(workspace_id, search_term).decode('utf-8'))
            return [{"text": i['label']['value'], "description": i['desc']['value'] if 'desc' in i else None,
                     "value": "<" + i['subject']['value'] + ">"} for i in
                    ret['results']['bindings']] if ret is not None else Response(status=404)
        except HTTPException as ex:
            return Response(ex.code)
