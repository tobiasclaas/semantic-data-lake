from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument
from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.exceptions import NotFound, Conflict

from api.services.decorators import parse_params
from utils.services.mapper import mapper
from database.data_access import user_data_access
from database.models import User
from .current import Current


class Users(Resource):
    
    @parse_params(
        Argument("email", type=str)
    )
    def get(self, email=None):
        """
        # ==================================================================================================

        :param email:
        :return:
        # ==================================================================================================

        """
        if email:
            user = user_data_access.get_by_email(email)
            return mapper(user)
        else:
            users = []
            for user in user_data_access.get_all():
                users.append(mapper(user))
            return jsonify(users)

    @parse_params(
        Argument("email", required=True, type=str),
        Argument("firstname", required=True, type=str),
        Argument("lastname", required=True, type=str),
        Argument("is_admin", required=True, type=bool),
    )
    def put(self, email, firstname, lastname, is_admin):
        """
         # ==================================================================================================

        :param email:
        :param firstname:
        :param lastname:
        :param is_admin:
        :return:
        # ==================================================================================================

        """
        user = user_data_access.get_by_email(email)
        user.firstname = firstname
        user.lastname = lastname
        user.is_admin = is_admin
        user.save()
        return jsonify(mapper(user))

    @parse_params(
        Argument("email", required=True, type=str),
        Argument("password", required=True, type=str),
        Argument("firstname", required=True, type=str),
        Argument("lastname", required=True, type=str),
        Argument("is_admin", required=True, type=bool),
    )
    def post(self, email, password, firstname, lastname, is_admin):
        """
    # ==================================================================================================
        :param email:
        :param password:
        :param firstname:
        :param lastname:
        :param is_admin:
        :return:
        # ==================================================================================================
        """
        try:
            user_data_access.get_by_email(email)
            raise Conflict(f"User with email {email} already exists")
        except NotFound:
            user = User(
                email=email,
                password_hash=sha256.hash(password),
                firstname=firstname,
                lastname=lastname,
                is_admin=is_admin
            )
            user.save()
            return jsonify(mapper(user))
    
    @parse_params(
        Argument("email", required=True, type=str)
    )
    def delete(self, email):
        """
    # ==================================================================================================
        :param email:
        :return:
    # ==================================================================================================
        """
        user = user_data_access.get_by_email(email)
        user.delete()
        return f"deleted user {email}"
