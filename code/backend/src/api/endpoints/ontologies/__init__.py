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
from requests import put, post, delete



def mapper(item):
    return{
        "id": str(item.id),
        "name": item.name,
    }
        

class Ontologies(Resource):
    def get(self, workspace_id):
        return jsonify([mapper(item) for item in ontology_data_access.get_all(workspace_id)])

    @parse_params( 
        Argument("file", type=FileStorage, location='files', required=True),
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
