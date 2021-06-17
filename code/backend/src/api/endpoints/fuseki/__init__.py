import traceback
import json
import os

from flask_restful import Resource
from flask_restful.reqparse import Argument
from werkzeug.datastructures import FileStorage
from requests import put, post, delete, patch

from api.services.decorators import parse_params


def create_query_string(databasename: str, graph_name: str, querystring: str):
    """
    This methods generates the query string for the keyword-search in put.
    :param databasename: name of the database
    :param graph_name: graph to be queried, default is "default graph"
    :param querystring: keywords to search for or when search-bool is false the query itself
    :returns: the query
    """
    if graph_name == '' or graph_name is None:
        graph_name = '?g'
        query = "SELECT ?s ?p ?o " \
            "WHERE { { Graph " + graph_name + " { ?s ?p ?o . FILTER (contains(?s,'" + querystring + "')) } } " \
            "UNION { Graph " + graph_name + " { ?s ?p ?o . FILTER (contains(?p, '" + querystring + "')) } } " \
            "UNION { Graph " + graph_name + " { ?s ?p ?o . FILTER (contains(?o, '" + querystring + "')) } } }"
    else:
        graph_name = 'http://localhost:3030/' + databasename + '#' + graph_name
        query = "SELECT ?s ?p ?o " \
            "WHERE { { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?s,'" + querystring + "')) } } " \
            "UNION { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?p, '" + querystring + "')) } } " \
            "UNION { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?o, '" + querystring + "')) } } }"

    return query


class Fuseki(Resource):
    @parse_params(Argument("databasename", type=str))
    def patch(self, databasename: str):
        """
        This method sends a request to the fuseki flask and creates a new workspace if no error occurs.
        :param databasename: is a string and name of the to be created workspace
        :returns statuscode of the request
        """
        p = post('http://localhost:3030/$/datasets', auth=('admin', 'pw123'),
                 data={'dbName': databasename, 'dbType': 'tdb'})

        return p.status_code

    @parse_params(
        Argument("databasename", type=str),
        Argument("querystring", type=str),
        Argument("graphname", type=str),
        Argument("search", type=bool))
    def post(self, databasename: str, querystring: str, graphname: str, search: bool):
        """
        This method queries fuseki for terms associated with the query string. If the parameter search is given,
        this method queries fuseki for any triple containing the query string.
        :param databasename: name of the database
        :param querystring: keywords to search for or when search-bool is false the query itself
        :param graphname: graph to be queried, default is "default graph"
        :param search: is a boolean whether to return all triples containing a given string or complete sparql query is
            given. True -> search for keywords(querystring), False -> query string is given.
        :return: json file or html status-code.
            JSON: dictionary with 3 keys, "s" for subject, "p" for predicate, "o" for object with values are
                again dicts with indices. s[0], p[0], o[0] belong together and is one triple of the result.
            Status Code: If error occurs.
        """
        if search:
            # replace admin and pw by environment variable defined in docker-compose.yaml
            p = post('http://localhost:3030/' + databasename, auth=('admin', 'pw123'),
                     data={'query': create_query_string(databasename, graphname, querystring)})

            try:
                data = json.loads(p.content)
                return data

            except Exception:
                traceback.print_exc()
                return p.status_code
        else:
            p = post('http://localhost:3030/' + databasename, auth=('admin', 'pw123'), data={'query': querystring})

            try:
                data = json.loads(p.content)

                return data
            except Exception:
                traceback.print_exc()
                return p.status_code

    @parse_params(
        Argument("databasename", type=str),
        Argument("file", type=FileStorage, location='files'),
        Argument("graphname", type=str, required=True),
        Argument("overwrite", type=bool))
    def put(self, databasename: str, file: FileStorage, graphname: str, overwrite: bool):
        """
        Upload a given file to a specified database.
        :param file: A file to be uploaded
        :param databasename: The name of the database
        :param graphname: The name of the graph were the file is inserted to. Fuseki is configured to take the default
        graph | as the Union over all subgraphs. Fail upload fails if no graphname is specified, thus this parameter is
        required.
        :param overwrite: If parameter is passed, the existing triples will be deleted and replaced with incoming file
        :return: Statuscode of the request
        """
        extension = os.path.splitext(file.filename)[1].lower()

        # other formats need to be tested
        if ".n3" == extension:
            headers = {'Content-Type': 'text/n3; charset=utf-8'}
        elif ".rdf" == extension:
            headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
        elif ".owl" == extension:
            headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
        elif ".jsonld" == extension:
            headers = {'Content-Type': 'application/ld+json; charset=utf-8'}
        # elif "nt" in extension.lower():
        #    headers = {'Content-Type': 'text/plain; charset=utf-8'}
        # elif "nq" in extension.lower():
        #    headers = {'Content-Type': 'application/n-quads; charset=utf-8'}
        # elif "trig" in extension.lower():
        #    headers = {'Content-Type': 'application/trig; charset=utf-8'}
        else:
            raise TypeError(extension.lower() + " is not supported")

        if not overwrite:
            p = post('http://localhost:3030/{}?graph={}'.format(databasename, graphname), data=file, headers=headers)
        else:
            p = put('http://localhost:3030/{}?graph={}'.format(databasename, graphname), data=file, headers=headers)

        return p.status_code

    @parse_params(
        Argument("databasename", type=str),
        Argument("graphname", type=str))
    def delete(self, databasename: str, graphname: str):
        """
        Delete a specified database.
        :param databasename: The name of the database to be deleted.
        :param graphname: The graph to be deleted.
        :return: Statuscode of the request.
        """
        if graphname != "" and graphname is not None:
            p = delete('http://localhost:3030/{}?graph={}'.format(databasename, graphname), auth=('admin', 'pw123'))
        else:
            p = delete('http://localhost:3030/$/datasets/{}'.format(databasename), auth=('admin', 'pw123'))

        return p.status_code
