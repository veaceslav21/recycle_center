from flask import request
from .models import Center
from .validators import CenterSchema
from flask import Blueprint

center_bp = Blueprint("center_blueprint", __name__)

center_schema = CenterSchema()
list_center_schema = CenterSchema(many=True)


@center_bp.route("/", methods=["GET"])
def center_list():
    centers = Center.query.all()
    return list_center_schema.dump(centers), 200


@center_bp.route("/", methods=["POST"])
def post():
    center_json = request.get_json()
    address = center_json['address']
    if Center.find_by_address(address):
        return {'message': "Center already exists"}, 400

    center_data = center_schema.load(center_json)
    center_data.save_to_db()

    return center_schema.dump(center_data), 201
