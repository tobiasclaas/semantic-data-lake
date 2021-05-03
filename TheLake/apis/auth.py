from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument
from services.decorators import parseParams
from models.user import User
from flask_jwt_extended import (JWTManager,create_access_token, jwt_required, create_refresh_token, get_jwt_identity, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies, jwt_refresh_token_required)

jwt = JWTManager()
user = User()

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    # pylint: disable=no-member
    if not User.objects(email__exact=identity):
        return None

    return User.objects(email__exact=identity).get()

@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404

class UserRegistration(Resource):
    @parseParams(Argument("email", required=True), Argument("password", required=True))
    def post(self, email, password):
        try:
            # pylint: disable=no-member
            User.objects(email__exact=email).get()
            return {'message': 'User {} already exists'.format(email)}
        except:
            try: 
                user = User(
                    email=email,
                    password=User().generateHash(password),
                    isAdmin=False,
                )
                # pylint: disable=no-member
                User.objects.insert(user)

                payload = {
                    "email": email,
                    "firstname": "",
                    "lastname": "",
                    "isAdmin": False,
                }

                accessToken = create_access_token(identity=payload)
                refreshToken = create_refresh_token(identity=payload)

                resp = jsonify({
                    'access_token_cookie': accessToken,
                })

                set_access_cookies(resp, accessToken)
                set_refresh_cookies(resp, refreshToken)

                return resp
            except Exception as e:
                return {'message': e.args[0]}



class UserLogin(Resource):
    @parseParams(Argument("email", required=True), Argument("password", required=True))
    def post(self, email, password):
        # pylint: disable=no-member
        currentUser = User.objects(email__exact=email)
        if not currentUser:
            return {'message': 'User {} doesn\'t exist'.format(email)}

        if user.verifyHash(password, currentUser.get().password):
            payload = {
                "email": email,
                "firstname": currentUser.get().firstname,
                "lastname": currentUser.get().lastname,
                "isAdmin": currentUser.get().isAdmin,
            }

            accessToken = create_access_token(identity=payload)
            refreshToken = create_refresh_token(identity=payload)

            resp = jsonify({
                'message': 'Logged in as {}'.format(currentUser.get().email),
                'access_token_cookie': accessToken,
            })

            set_access_cookies(resp, accessToken)
            set_refresh_cookies(resp, refreshToken)
            return resp

        else:
            return {'message': 'Wrong credentials'}


class UserLogout(Resource):
    def post(self):
        try:
            resp = jsonify({'logout': True})
            unset_jwt_cookies(resp)
            return resp
        except:
            return jsonify({'error': 'Something went wrong deleting token'})


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            currentUser = get_jwt_identity()
            accessToken = create_access_token(identity=currentUser)
            resp = jsonify({'message': 'Token Refreshed!'})
            set_access_cookies(resp, accessToken)
            return resp
        except:
            return jsonify({'error': 'Something went wrong refreshing token'})

class GetCredentialsFromToken(Resource):
    @jwt_required
    def post(self):
        try:
            currentUser = User.objects(email__exact = get_jwt_identity()["email"])
            resp = jsonify(
                {'user': {
                    "email": currentUser.get().email,
                    "firstname": currentUser.get().firstname,
                    "lastname": currentUser.get().lastname,
                    "isAdmin": currentUser.get().isAdmin,
                }}
                )
            return resp
        except:
            return jsonify({'error': 'Something went wrong'})
