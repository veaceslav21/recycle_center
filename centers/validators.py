from marshmallow import Schema, fields, validate
from .models import Center


class CenterSchema(Schema):
    id = fields.Int()
    address = fields.Str(required=True, validate=validate.Length(max=100))
    # types of materials
    glass = fields.Boolean(required=True)
    plastic = fields.Boolean(required=True)
    paper = fields.Boolean(required=True)


class UpdateCenterSchema(Schema):
    id = fields.Int()
    address = fields.Str(validate=validate.Length(max=100))
    # types of materials
    glass = fields.Boolean()
    plastic = fields.Boolean()
    paper = fields.Boolean()

