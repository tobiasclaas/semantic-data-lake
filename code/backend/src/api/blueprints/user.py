from flask import Blueprint
from flask_restful import Api

from api.endpoints.users import Users, Current

USER_BLUEPRINT = Blueprint("user.py", __name__)

users_routes = ["/users", "/users/<email>"]
Api(USER_BLUEPRINT).add_resource(Users, *users_routes)

current_routes = ["/users/current"]
Api(USER_BLUEPRINT).add_resource(Current, *current_routes)

