from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class ApplicationSchema(Schema):
    id = fields.Int()
    material_type = fields.String(required=True, validate=OneOf(["paper", "plastic", "glass"]))
    capacity = fields.Float(required=True)
    center_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
