from os import abort
from flask import jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import Argument
from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.exceptions import HTTPException

from utils.services.mapper import mapper
from api.services.decorators import parse_params
from database.data_access import workspace_data_access, user_data_access


class Workspaces(Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()['email']
        return jsonify([mapper(item) for item in workspace_data_access.get_all(user_data_access.get_by_email(email))])

    @jwt_required
    @parse_params(
        Argument("name", default=None, type=str, required=True)
    )
    def post(self, name):
        email = get_jwt_identity()['email']
        return jsonify(mapper(workspace_data_access.create(name, user_data_access.get_by_email(email))))

    @jwt_required
    @parse_params(
        Argument("workspace_id", default=None, type=str, required=True)
    )
    def delete(self, workspace_id):
        try:
            email = get_jwt_identity()['email']
            workspace_data_access.delete(workspace_id, user_data_access.get_by_email(email))
            return Response(status=200)
        except HTTPException as inst:
            return Response(status=inst.code)
