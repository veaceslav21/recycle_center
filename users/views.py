from flask import request
from users.auth import _create_user, _login_user, _reset_password
from flask import Blueprint
from .models import User
from .validators import UserSchema
from flask_jwt_extended import get_jwt_identity, jwt_required
import basehash
from flask import jsonify


user_bp = Blueprint("user_blueprint", __name__)
user_schema = UserSchema()


@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    return _create_user(data), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return _login_user(data), 201


@user_bp.route("/password_reset", methods=["POST"])
@jwt_required()
def password_rest():
    current_user = User.query.get(get_jwt_identity())
    data = request.get_json()
    return _reset_password(data, current_user), 201


@user_bp.route("/list", methods=["GET"])
@jwt_required()
def get_users():  # Should work only for admin and staff
    users = User.query.all()
    return user_schema.dump(users, many=True), 200


@user_bp.route("/info", methods=["GET"])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if not user:
        return {"message": "User does not exists"}, 404
    return user_schema.dump(user, many=False), 200


@user_bp.route("/referral", methods=["GET"])
@jwt_required()
def get_referral_code():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    hash_fn = basehash.base36()
    referral_code = hash_fn.hash(user.id)
    return jsonify({"referral_code": referral_code})