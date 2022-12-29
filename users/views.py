from flask import request
from users.auth import create_user, login_user, reset_password
from flask import Blueprint
from .models import User
from .validators import UserRegisterSchema


user_bp = Blueprint("user_blueprint", __name__)
user_schema = UserRegisterSchema()


@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    return create_user(data)


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data)


@user_bp.route("/password_reset", methods=["POST"])
def password_rest():
    if request.headers['Authorization']:
        token = request.headers['Authorization'].lstrip("JWT ")
        data = request.get_json()
        return reset_password(data, token)

    return {"message": "Authorization required, please login."}


@user_bp.route("/list", methods=["GET"])
def get_users():
    users = User.query.all()
    return user_schema.dump(users, many=True)


@user_bp.route("/<int:id>", methods=["GET"])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return {"message": "User does not exists"}, 404
    return user_schema.dump(user, many=False), 200