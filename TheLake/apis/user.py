#coding: utf-8
from flask_restful import abort, Resource
from flask_restful.reqparse import Argument
from flask_restful.inputs import boolean
from services.decorators import parseParams
from bl.user import UserBusinessLogic
from flask_jwt_extended import jwt_required, get_jwt_identity, get_csrf_token, current_user
from flask import jsonify

class User(Resource):
    bl = UserBusinessLogic()

    @jwt_required
    def get(self, email=None):
        if email == None:
            return jsonify(self.bl.getList())
        else:
            return jsonify(self.bl.get(email))

    @jwt_required
    def delete(self, email):
        if self.bl.delete(email) == True:
            return "", 204
        else:
            abort(404, message="User with that email {} was not deleted".format(email))

    @jwt_required
    @parseParams(
        Argument("password", default=None, type=str, required=False), 
        Argument("isAdmin", default=None, type=boolean, required=False),
        Argument("firstname", default=None, type=str, required=False), 
        Argument("lastname", default=None, type=str, required=False),
    )
    def put(self, email, isAdmin, firstname, lastname, password):
        return jsonify(self.bl.put(email, isAdmin, firstname, lastname, password))
    
    @jwt_required
    @parseParams( 
        Argument("email", default=None, type=str, required=True),
        Argument("password", default=None, type=str, required=True), 
        Argument("isAdmin", default=None, type=boolean,required=True),
        Argument("firstname", default=None, type=str, required=True),
        Argument("lastname", default=None, type=str, required=True)
    )
    def post(self, email, password, isAdmin, firstname, lastname):
        return jsonify(self.bl.post(email, password, isAdmin, firstname, lastname))
