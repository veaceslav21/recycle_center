from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class PasswordResetSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=6))