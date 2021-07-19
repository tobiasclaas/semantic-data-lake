from flask import jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
)
from flask_restful import Resource
from flask_restful.reqparse import Argument
from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.exceptions import Unauthorized

from api.services.decorators import parse_params
from utils.services.mapper import mapper
from database.data_access import user_data_access


class Login(Resource):

    @parse_params(
        Argument("email", required=True, type=str),
        Argument("password", required=True, type=str),
    )
    def post(self, email, password):
        """
        # ==================================================================================================
        #Login Page Enter credential
        :param email:
        :param password:
        :return:
        # ==================================================================================================
        """
        user = user_data_access.get_by_email(email)

        if not sha256.verify(password, user.password_hash):
            raise Unauthorized(f"Wrong email or password")

        access_token = create_access_token(identity=mapper(user))
        refresh_token = create_refresh_token(identity=mapper(user))

        response = jsonify({

            "user": mapper(user),
            "access_token": access_token
        })

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response
