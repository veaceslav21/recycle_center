from flask import request
from flask_restful import Resource
from users.auth import create_user, login_user


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