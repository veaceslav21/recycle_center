from flask import request
from .models import Center
from .validators import CenterSchema, UpdateCenterSchema
from flask import Blueprint

center_bp = Blueprint("center_blueprint", __name__)

center_schema = CenterSchema()
list_center_schema = CenterSchema(many=True)
update_schema = UpdateCenterSchema()


@center_bp.route("/list", methods=["GET"])
def center_list():
    centers = Center.query.all()
    return list_center_schema.dump(centers), 200


@center_bp.route("/<int:id>", methods=["GET"])
def get_center(id):
    center = Center.query.filter_by(id=id).first()
    return center_schema.dump(center), 200


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


@center_bp.route("update/<int:id>", methods=["PUT"])
def center_update(id):
    data = request.get_json()
    center = Center.query.filter_by(id=id).first()
    if not center:
        return {"message": "Center does not exists"}
    validated_data = update_schema.load(data)

    for kye, value in validated_data.items():
        setattr(center, kye, value)
    center.save_to_db()
    return center_schema.dump(center)


@center_bp.route("delete/<int:id>", methods=["DELETE"])
def center_delete(id):
    center = Center.query.filter_by(id=id).first()
    if not center:
        return {"message": "Center does not exists"}
    center.delete_from_db()
    return {"message": f"<{center}> was deleted"}, 404
