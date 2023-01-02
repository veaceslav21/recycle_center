from flask import Blueprint
from .models import Application
from .validators import ApplicationSchema
from flask import request
from .remuneration import user_remuneration
from users.models import User
import jwt
from os import environ
from flask import jsonify

recycle_bp = Blueprint("recycle_bp", __name__)
request_schema = ApplicationSchema()


@recycle_bp.route("/list", methods=["GET"])
def get_requests():
    requests = Application.query.all()
    return request_schema.dump(requests, many=True)


@recycle_bp.route("/create", methods=["POST"])
def create_request():
    data = request.get_json()
    try:
        validated_data = request_schema.load(data)  # .load() return data if it passed validation else error
    except Exception as error:
        return jsonify(error.args), 400

    new_request = Application(**validated_data)
    new_request.save_to_db()

    try:
        token = request.headers['Authorization'].lstrip("JWT ")
    except KeyError:
        return jsonify({"error": "Your are not logged in, pls login and repeat."}), 400
    token_info = jwt.decode(token, environ.get("SECRET_KEY"))
    user = User.query.filter_by(id=token_info['user_id']).first()
    material_type = validated_data['material_type']
    capacity = validated_data['capacity']
    user_remuneration(user, material_type, capacity)
    return request_schema.dump(new_request), 201

