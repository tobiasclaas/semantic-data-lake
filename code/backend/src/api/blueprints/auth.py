from flask import Blueprint
from flask_restful import Api

from api.endpoints.auth import Login, Logout, TokenRefresh

AUTH_BLUEPRINT = Blueprint("auth.py", __name__)

login_routes = ["/auth/login"]
Api(AUTH_BLUEPRINT).add_resource(Login, *login_routes)

logout_routes = ["/auth/logout"]
Api(AUTH_BLUEPRINT).add_resource(Logout, *logout_routes)

token_refresh_routes = ["/auth/token_refresh"]
Api(AUTH_BLUEPRINT).add_resource(TokenRefresh, *token_refresh_routes)
