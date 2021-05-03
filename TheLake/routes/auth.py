#coding: utf-8
from flask import Blueprint
from flask_restful import Api

from apis.auth import UserRegistration, UserLogin, UserLogout, TokenRefresh, GetCredentialsFromToken

AUTH_BLUEPRINT = Blueprint("auth", __name__)
routes = ['/auth/register',]
Api(AUTH_BLUEPRINT).add_resource(
    UserRegistration, *routes,
)
routes = ['/auth/login',]
Api(AUTH_BLUEPRINT).add_resource(
    UserLogin, *routes,
)
routes = ['/auth/logout',]
Api(AUTH_BLUEPRINT).add_resource(
    UserLogout, *routes,
)
routes = ['/auth/refresh',]
Api(AUTH_BLUEPRINT).add_resource(
    TokenRefresh, *routes,
)
routes = ['/auth/getCredentialsFromToken']
Api(AUTH_BLUEPRINT).add_resource(
    GetCredentialsFromToken, *routes,
)


