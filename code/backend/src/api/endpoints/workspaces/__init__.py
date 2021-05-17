from os import abort
from flask import jsonify, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument
from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, Conflict

from api.services.decorators import parse_params
from database.data_access import workspace_data_access


def mapper(item):
    return{
        "id": str(item.id),
        "name": item.name,
    }
        

class Workspaces(Resource):
    def get(self):
        return jsonify([mapper(item) for item in workspace_data_access.get_all()])

    @parse_params( 
        Argument("name", default=None, type=str, required=True),
    )
    def post(self, name):
        return jsonify(mapper(workspace_data_access.create(name)))

    @parse_params( 
        Argument("id", default=None, type=str, required=True),
    )
    def delete(self, id):
        try:
            workspace_data_access.delete(id)
            return Response(status=200)
        except HTTPException as inst:
            return Response(status=inst.code)




