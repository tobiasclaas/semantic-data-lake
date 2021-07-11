from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from werkzeug.exceptions import InternalServerError


class Logout(Resource):

    
    def post(self):
        """
        # ==================================================================================================
        Main return function in logout page.
        :return:
        # ==================================================================================================
        """
        try:
            # ==================================================================================================
            #Successfully logout
            # ==================================================================================================
            response = jsonify({
                "logged out": True
            })
            unset_jwt_cookies(response)
            return response
        except Exception as err:
            # ==================================================================================================
            #error while logging out
            # ==================================================================================================
            raise InternalServerError(f"Exception while logging out: \n\t {err}")
