from db import db
import jwt
import datetime
from .models import User
from .validators import UserRegisterSchema, UserLoginSchema
from os import environ


def create_user(input_data):
    validation_schema = UserRegisterSchema()
    error = validation_schema.validate(input_data)  # This return dict() of errors if input data didn't pass validation
    if error:
        return {"message": "Input data is not valid"}, 400

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

    return {"message": "You have registered successfully"}, 201


def login_user(input_data):
    validation_schema = UserLoginSchema()
    error = validation_schema.validate(input_data)

    if error:
        return {"message": "Input data is not valid"}, 400

    user = User.query.filter_by(email=input_data['email']).first()
    if not user:
        return {"message": "Wrong email/password or user don't exists"}

    if user.check_password(input_data['password']):

        token = jwt.encode(
            {'public_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            environ.get("SECRET_KEY")
        )
        return {"token": token.decode("UTF-8")}

