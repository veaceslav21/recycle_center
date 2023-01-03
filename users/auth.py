from db import db
import jwt
import datetime as dt
from .models import User
from .validators import UserRegisterSchema, UserLoginSchema, PasswordResetSchema
from flask_bcrypt import generate_password_hash
from os import environ
from flask import request, jsonify


def create_user(input_data):
    validation_schema = UserRegisterSchema()
    try:
        dt.datetime.strptime(input_data['birthday'], "%Y-%m-%d")
        input_data['birthday'] = str(dt.datetime.strptime(input_data['birthday'], "%Y-%m-%d"))
    except:
        return {"custom_error": "Wrong datetime format"}, 400

    input_data = validation_schema.load(input_data)  # return dict() with data if input data  pass validation

    check_username_exists = User.query.filter_by(username=input_data["username"]).first()
    if check_username_exists:
        return {"message": "Unavailable username"}, 400

    check_email_exists = User.query.filter_by(email=input_data["email"]).first()
    if check_email_exists:
        return {"message": "Unavailable email"}, 400

    new_user = User(**input_data)
    new_user.hash_password()
    db.session.add(new_user)
    db.session.commit()
    del input_data["password"]
    return {"message": "You have registered successfully",
            "new_user": validation_schema.dump(new_user)}, 201


def login_user(input_data):
    validation_schema = UserLoginSchema()
    error = validation_schema.validate(input_data)

    if error:
        return {"message": "Input data is not valid"}, 400

    user = User.query.filter_by(email=input_data['email']).first()
    if user and user.check_password(input_data['password']):
        token = jwt.encode(
            {'user_id': user.id, 'exp': dt.datetime.utcnow() + dt.timedelta(minutes=30)},
            environ.get("SECRET_KEY")
        )
        return {"token": token.decode("UTF-8")}

    return {"message": "Wrong email/password or user don't exists"}


def reset_password(input_data, token):
    validation_schema = PasswordResetSchema()
    error = validation_schema.validate(input_data)
    if error:
        return {"message": "Wrong input data"}

    token_info = jwt.decode(token, environ.get("SECRET_KEY"))
    user = User.query.filter_by(id=token_info['user_id']).first()

    if not user:
        return {"message": "No user found"}, 400

    user.password = generate_password_hash(input_data['new_password']).decode('utf8')
    db.session.commit()

    return {"message": "Password has been changed successfully"}, 200


def get_current_user():
    if request.headers['Authorization']:
        token = request.headers['Authorization'].lstrip("JWT ")
        token_info = jwt.decode(token, environ.get("SECRET_KEY"))
        user = User.query.filter_by(id=token_info['user_id']).first()
        return user

    return jsonify({"message": "Authorization required, please login."})