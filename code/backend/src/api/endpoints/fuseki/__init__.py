import traceback
import json
import os
import re

from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask import request
from werkzeug.datastructures import FileStorage
from requests import put, post, delete, get
from http import HTTPStatus
# from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import pprint

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
                                                                                                                                                                                               "UNION { Graph " + graph_name + " { ?s ?p ?o . FILTER (contains(?o, '" + querystring + "')) } } } "
    else:
        graph_name = 'http://localhost:3030/' + databasename + '/' + graph_name
        query = "SELECT ?s ?p ?o " \
                "WHERE { { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?s,'" + querystring + "')) } } " \
                                                                                                          "UNION { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?p, '" + querystring + "')) } } " \
                                                                                                                                                                                                   "UNION { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?o, '" + querystring + "')) } } } "

    return query


def replace_graphname(graphname: str, query: str):
    """
    Replaces the name of Graph with actual reference, e.g. "http://local..."
    :param graphname:
    :param query:
    :return:
    """
    # TODO, do we want to implement this? Not that easy
    return query


class Fuseki(Resource):
    @parse_params(Argument("databasename", type=str))
    def post(self, databasename: str):
        """
        This method sends a request to the fuseki flask and creates a new workspace if no error occurs.
        :param databasename: is a string and name of the to be created workspace
        :returns statuscode of the request
        """
        if databasename == "" or databasename is None:
            print("No databasename given")
            return HTTPStatus.BAD_REQUEST

        p = post('http://localhost:3030/$/datasets', auth=('admin', 'pw123'),
                 data={'dbName': databasename, 'dbType': 'tdb'})

        return p.status_code

    @parse_params(
        Argument("databasename", type=str),
        Argument("querystring", type=str),
        Argument("graphname", type=str),
        Argument("search", type=bool))
    def get(self, databasename: str, querystring: str, graphname: str, search: bool):
        """
        This method queries fuseki for terms associated with the query string. If the parameter search is given,
        this method queries fuseki for any triple containing the query string.
        :param databasename: name of the database
        :param querystring: keywords to search for or when search-bool is false the query itself
        :param graphname: graph to be queried, default is "default graph"
        :param search: is a boolean whether to return all triples containing a given string or complete sparql query is
            given. True -> search for keywords(querystring), False -> query string is given
        :return: pandas dataframe, TODO currently buggy
        """
        if search:
            # TODO replace admin and pw by environment variable defined in docker-compose.yaml,
            #  better solution required. lets ask maher
            p = post('http://localhost:3030/' + databasename, auth=('admin', 'pw123'),
                     data={'query': create_query_string(databasename, graphname, querystring)})

            data = json.loads(p.content)
            # pprint.pprint(data['results']['bindings'][0])  # TODO delete, for debugging
            df = pd.DataFrame(data['results']['bindings'], columns=['s', 'p', 'o'])

            return df.to_json()  # TODO looks good to me @Sayed
        else:
            # replace admin and pw by environment variable defined in docker-compose.yaml
            querystring = replace_graphname(graphname, querystring)

            p = post('http://localhost:3030/' + databasename, auth=('admin', 'pw123'), data={'query': querystring})

            if not p.ok:  # if request was bad, return None
                return None

            pprint.pprint(p.content)
            data = json.loads(p.content)

            # TODO delete if satisfied @sayed
            # pprint.pprint(data)
            # array = json.dumps(data)
            # array2 = json.loads(array)
            # pd.json_normalize(array2, ['results', 'bindings'])
            # df = pd.json_normalize(array['results']['bindings'])  # weiß net warum das nich funzt

            # try:
            #    return df
            # except Exception as ex:
            #    traceback.print_exception(type(ex), ex, ex.__traceback__)
            df = pd.DataFrame(data['results']['bindings'], columns=['s', 'p', 'o'])

            return df.to_json()  # TODO looks good to me @Sayed

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
        :param databasename: The name of the database to be deleted
        :param graphname: The graph to be deleted
        :return: Statuscode of the request
        """
        # TODO delete specific graphs?
        if graphname:
            p = delete('http://localhost:3030/{}?graph={}'.format(databasename, graphname), auth=('admin', 'pw123'))
        else:
            p = delete('http://localhost:3030/$/datasets/{}'.format(databasename), auth=('admin', 'pw123'))

        return p.status_code
