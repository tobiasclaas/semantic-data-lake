from os import abort
import os

from flask import json, jsonify, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument
from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, Conflict
from werkzeug.datastructures import FileStorage

from api.services.decorators import parse_params
from database.data_access import ontology_data_access

import traceback
import json
from requests import put, post, delete, patch
import pandas as pd
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
        graph_name = 'http://localhost:3030/' + databasename + '/' + graph_name
        query = "SELECT ?s ?p ?o " \
                "WHERE { { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?s,'" + querystring + "')) } } " \
                "UNION { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?p, '" + querystring + "')) } } " \
                "UNION { Graph <" + graph_name + "> { ?s ?p ?o . FILTER (contains(?o, '" + querystring + "')) } } }"

    return query



def mapper(item):
    return{
        "id": str(item.id),
        "name": item.name,
    }
        

class Ontologies(Resource):
    def get(self, workspace_id):
        return jsonify([mapper(item) for item in ontology_data_access.get_all(workspace_id)])

    @parse_params( 
        Argument("file", type=FileStorage, location='files', required=False),
        Argument("name", default=None, type=str, required=False),
        Argument("querystring", type=str, required=False),
        Argument("graphname", type=str, required=False),
        Argument("search", type=str, required=False))
    def post(self, name, file, workspace_id, querystring, graphname, search):

        if search:
            # TODO replace admin and pw by environment variable defined in docker-compose.yaml,
            #  better solution required. lets ask maher
            # replace admin and pw by environment variable defined in docker-compose.yaml
            p = post('http://localhost:3030/' + workspace_id, auth=('admin', 'pw123'),
                     data={'query': create_query_string(workspace_id, graphname, search)})

            try:
                data = json.loads(p.content)
                return data

            except Exception:
                traceback.print_exc()
                return p.status_code
        elif querystring:
            p = post('http://localhost:3030/' + workspace_id, auth=('admin', 'pw123'), data={'query': querystring})

            try:
                data = json.loads(p.content)
            
                return data
            except Exception:
                traceback.print_exc()
                return p.status_code
        else:
            return jsonify(mapper(ontology_data_access.add(name, file, workspace_id)))

    def delete(self, id, workspace_id):
        try:
            ontology_data_access.delete(id, workspace_id)
            return Response(status=200)
        except HTTPException as inst:
            return Response(status=inst.code)
   