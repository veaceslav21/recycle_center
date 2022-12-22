from flask import request
from users.auth import create_user, login_user, reset_password
from flask import Blueprint

user_bp = Blueprint("user_blueprint", __name__)


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
