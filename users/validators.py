from marshmallow import Schema, fields, validate
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=5))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    birthday = fields.DateTime(required=True)
    is_staff = fields.Boolean(default=False)
    is_admin = fields.Boolean(default=False)


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class PasswordResetSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=6))