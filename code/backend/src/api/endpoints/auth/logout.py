from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from werkzeug.exceptions import InternalServerError


class Logout(Resource):
    
    def post(self):
        try:
            response = jsonify({
                "logged out": True
            })
            unset_jwt_cookies(response)
            return response
        except Exception as err:
            raise InternalServerError(f"Exception while logging out: \n\t {err}")
