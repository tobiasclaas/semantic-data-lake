#coding: utf-8
from flask import Blueprint
from flask_restful import Api

from apis.user import User

USER_BLUEPRINT = Blueprint("user", __name__)
routes = ['/user','/user/<email>',]
Api(USER_BLUEPRINT).add_resource(
    User, *routes
)