from marshmallow import Schema, fields, validate
import datetime


class UserRegisterSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=validate.Length(min=5))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    birthday = fields.DateTime(required=True)
    rating = fields.Float(dump_only=True)
    is_staff = fields.Boolean()
    is_admin = fields.Boolean()


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class PasswordResetSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=6))