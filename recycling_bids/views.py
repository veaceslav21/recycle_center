from flask import Blueprint
from .models import Application
from .validators import ApplicationSchema
from flask import request
from .remuneration import user_remuneration
from users.models import User
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

recycle_bp = Blueprint("recycle_bp", __name__)
request_schema = ApplicationSchema()


@recycle_bp.route("/list", methods=["GET"])
@jwt_required()
def get_requests():
    requests = Application.query.all()
    return request_schema.dump(requests, many=True)


@recycle_bp.route("/create", methods=["POST"])
@jwt_required()
def create_request():
    data = request.get_json()
    try:
        validated_data = request_schema.load(data)  # .load() return data if it passed validation else error
    except Exception as error:
        return jsonify(error.args), 400

    new_request = Application(**validated_data)
    new_request.save_to_db()

    user = User.query.get(get_jwt_identity())
    material_type = validated_data['material_type']
    capacity = validated_data['capacity']
    user_remuneration(user, material_type, capacity)
    return request_schema.dump(new_request), 201

