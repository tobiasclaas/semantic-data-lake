import json
from flask import json, jsonify, Response
from flask_restful import Resource
from flask_restful.reqparse import Argument
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, Conflict
from werkzeug.datastructures import FileStorage
from requests import put, post, delete as delete_request
from api.services.decorators import parse_params
from database.data_access import ontology_data_access
from database.data_access import annotation_data_access
from business_logic.services.mapper import mapper as mapper_general
from requests import put, post, patch
from api.services.decorators import parse_params


def create_query_string(database_name: str, graph_name: str, keyword: str):
    """
    This methods generates the query string for the keyword-search in put.
    :param database_name: name of the database
    :param graph_name: graph to be queried, default is "default graph",
        like "<http://localhost:3030/60d5c79a7d2c38ee678e87a8/60d5c79d7d2c38ee678e87a9>"
    :param keyword: keywords to search for or when search-bool is false the query itself
    :returns: the query
    """
    if graph_name == '' or graph_name is None:
        graph_name = '?g'

    query = """ SELECT ?subject ?predicate ?object ?g
                WHERE {
                    GRAPH """ + graph_name + """ {
                        ?subject ?predicate ?object .
                        FILTER (
                            regex(str(?subject), """ + keyword + """) ||
                            regex(str(?predicate), """ + keyword + """) ||
                            regex(str(?object),  """ + keyword + """))
                  }
                }
                """

    return query


def select_query_fuseki(workspace_id, graph_name, search):
    # replace admin and pw by environment variable defined in docker-compose.yaml
    return post('http://localhost:3030/' + workspace_id, auth=('admin', 'pw123'),
                data={'query': create_query_string(workspace_id, graph_name, search)})


def mapper(item):
    return {
        "id": str(item.id),
        "name": item.name,
    }


def get_suggestions(workspace_id, search_term):
    """
    This function provides multiple suggestions for a auto-completion of ontology-attributes in fuseki
    :word: search string
    :return:
    """
    querystring = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?subject ?label
        WHERE {
          ?subject a ?x ;
            rdfs:label ?label .
          FILTER (regex(str(?subject), '""" + search_term + """', 'i') || 
            regex(?label, '""" + search_term + """', 'i'))
        }
        ORDER BY strlen(?label)
        LIMIT 10    """
    p = post('http://localhost:3030/' + workspace_id, auth=('admin', 'pw123'), data={'query': querystring})

    try:
        data = json.loads(p.content)
        return data
    except Exception:
        return p.status_code


class Ontologies(Resource):
    def get(self, workspace_id):
        return jsonify([mapper(item) for item in ontology_data_access.get_all(workspace_id)])

    @parse_params(
        Argument("file", type=FileStorage, location='files', required=False),
        Argument("name", default=None, type=str, required=False),
    )
    def post(self, name, file, workspace_id):
        return jsonify(mapper(ontology_data_access.add(name, file, workspace_id)))

    def delete(self, id, workspace_id):
        try:
            ontology_data_access.delete(id, workspace_id)
            return Response(status=200)
        except HTTPException as inst:
            return Response(status=inst.code)
   

class OntologiesSearch(Resource):
    @parse_params( 
        Argument("q", default=None, type=str, required=True),
    )
    def get(self, workspace_id, q):
        return jsonify([{"uri":"http://demo", "text":"demo"}, {"uri":"http://test", "text":"test"}])


class Annotation(Resource):
    @parse_params(
        Argument('datamart_id', required=True, type=str),
        Argument('data_attribute', type=str, default=None)
    )
    def get(self, workspace_id, datamart_id, data_attribute):
        # API function for accessing annotations of specific attribute
        return mapper_general(annotation_data_access.get(datamart_id, data_attribute))

    @parse_params(
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
    def delete(self, workspace_id, datamart_id, data_attribute, property_description, ontology_attribute):
        return annotation_data_access.delete(datamart_id, data_attribute, property_description,
                                             ontology_attribute)


class Completion(Resource):
    @parse_params(
        Argument('workspace_id', required=True, type=str),
        Argument('search_term', required=True, type=str)
    )
    def get(self, workspace_id, search_term=''):
        return get_suggestions(workspace_id, search_term)
