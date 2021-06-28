from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.exceptions import InternalServerError

from business_logic.services.mapper import mapper
from database.data_access import user_data_access


class Current(Resource):
    
    def post(self):
        try:
            email = get_jwt_identity()["email"]
            user = user_data_access.get_by_email(email)
            return jsonify(mapper(user))
        except Exception as err:
            raise InternalServerError(f"Exception while get user from token: \n\t {err}")
