from db import db
import datetime as dt
from .models import User
from .validators import UserSchema, PasswordResetSchema
from flask_bcrypt import generate_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token
from basehash import base36


def _create_user(input_data):
    validation_schema = UserSchema()
    try:
        dt.datetime.strptime(input_data['birthday'], "%Y-%m-%d")
        input_data['birthday'] = str(dt.datetime.strptime(input_data['birthday'], "%Y-%m-%d"))
    except:
        return {"custom_error": "Wrong datetime format"}, 400

    input_data = validation_schema.load(input_data)  # return dict() with data if input data  pass validation

    check_username_exists = User.query.filter_by(username=input_data["username"]).first()
    if check_username_exists:
        return jsonify({"message": "Unavailable username"}, 400)

    check_email_exists = User.query.filter_by(email=input_data["email"]).first()
    if check_email_exists:
        return jsonify({"message": "Unavailable email"}), 400

    if input_data.get("parent_referral", None):
        unhash_fn = base36()
        input_data["parent_referral"] = unhash_fn.unhash(input_data["parent_referral"])


    new_user = User(**input_data)
    new_user.hash_password()
    db.session.add(new_user)
    db.session.commit()
    del input_data["password"]

    return jsonify({"message": "You have registered successfully",
            "new_user": validation_schema.dump(new_user)})


def _login_user(data):
    login_schema = UserSchema(only=("email", "password"))
    data = login_schema.load(data)

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.id)
        return {"token": access_token, "user_id": user.id}

    return jsonify({"msg": "Bad email or password"}), 401


def _reset_password(data, user):
    validation_schema = PasswordResetSchema()
    error = validation_schema.validate(data)  # check difference between .validation() and . load()
    if error:
        return {"message": "Wrong input data"}

    if not user.check_password(data["old_password"]):
        return jsonify({"message": "Wrong old password, try again."})

    user.password = generate_password_hash(data['new_password']).decode('utf8')
    db.session.commit()

    return jsonify({"message": "Password has been changed successfully"})
