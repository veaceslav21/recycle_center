from flask import request, jsonify
from flask_restful import Resource
from users.auth import create_user, login_user, reset_password


class SignUpUser(Resource):

    @classmethod
    def post(cls):
        data = request.get_json()
        return create_user(data)


class LoginUser(Resource):

    @classmethod
    def post(cls):
        data = request.get_json()
        return login_user(data)


class ResetPassword(Resource):
    @staticmethod
    def post():
        if request.headers['Authorization']:
            token = request.headers['Authorization'].lstrip("JWT ")
            data = request.get_json()
            return reset_password(data, token)

        return {"message": "Authorization required, please login."}
