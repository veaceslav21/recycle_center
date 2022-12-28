from marshmallow import Schema, fields


class ApplicationSchema(Schema):
    id = fields.Int()
    material_type = fields.Str(required=True)
    capacity = fields.Float(required=True)
    center_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
