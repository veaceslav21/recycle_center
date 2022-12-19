from flask import request
from.models import Center
from flask_restful import Resource
from .validators import CenterSchema


center_schema = CenterSchema()
list_center_schema = CenterSchema(many=True)


class CenterResource(Resource):

    def get(self):
        centers = Center.query.all()
        return center_schema.dump(centers), 200

    def post(self):
        center_json = request.get_json()
        address = center_json['address']
        if Center.find_by_address(address):
            return {'message': "Center already exists"}, 400

        center_data = center_schema.load(center_json)
        center_data.save_to_db()

        return center_schema.dump(center_data), 201