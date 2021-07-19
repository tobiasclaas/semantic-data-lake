from flask import Blueprint
from flask_restful import Api

from api.endpoints.users import Users

USER_BLUEPRINT = Blueprint("user", __name__)

users_routes = ["/users", "/users/<email>"]
Api(USER_BLUEPRINT).add_resource(Users, *users_routes)
