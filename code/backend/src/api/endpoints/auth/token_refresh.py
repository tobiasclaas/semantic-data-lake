from flask import jsonify
from flask_jwt_extended import (create_access_token, get_jwt_identity, set_access_cookies,
                                jwt_refresh_token_required)
from flask_restful import Resource
from werkzeug.exceptions import InternalServerError


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            user = get_jwt_identity()
            token = create_access_token(identity=user)
            response = jsonify({
                "message": "Token refresh!"
            })

            set_access_cookies(response, token)

            return response
        except Exception as err:
            raise InternalServerError(f"Exception while refreshing token: \n\t {err}")
