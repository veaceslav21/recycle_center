from flask import request
from .models import Center
from .validators import CenterSchema
from flask import Blueprint

center_bp = Blueprint("center_blueprint", __name__)

center_schema = CenterSchema()
list_center_schema = CenterSchema(many=True)


@center_bp.route("/list", methods=["GET"])
def center_list():
    centers = Center.query.all()
    return list_center_schema.dump(centers), 200


@center_bp.route("create/", methods=["POST"])
def center_create():
    data = request.get_json()
    address = data['address']
    address = Center.query.filter_by(address=address).first()
    if address:
        return {'message': "Center already exists"}, 400

    center_data = center_schema.load(data)  # .load() return data if it passed validation else error
    new_center = Center(**center_data)
    new_center.save_to_db()

    return center_schema.dump(new_center), 201


# @center_bp.route("update/", methods=["PUT"])
# def center_update():
#     data = request.get_json()
#


