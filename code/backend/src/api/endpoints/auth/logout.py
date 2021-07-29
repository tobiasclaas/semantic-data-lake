from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from werkzeug.exceptions import InternalServerError


class Logout(Resource):
    """
    Class to log out a user.
    """

    def post(self):
        """
        API to logout a user.

        :return: The resposne of the request
        """
        try:
            response = jsonify({
                "logged out": True
            })
            unset_jwt_cookies(response)
            return response
        except Exception as err:
            raise InternalServerError(f"Exception while logging out: \n\t {err}")
