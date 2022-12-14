from flask_marshmallow.sqla import SQLAlchemySchema
from marshmallow import Schema, fields, validates_schema, ValidationError, EXCLUDE
from marshmallow.validate import Email, Length, Range
from marshmallow_sqlalchemy import auto_field

from .base_schemas import Fail, Success
from ..model.user import User


class UserSchema(SQLAlchemySchema):
    class Meta:
        # unknown = EXCLUDE
        model = User
        load_instance = True
        # include_fk = True

    id_ = fields.Integer(required=True, dump_only=True, attribute="id", data_key="id")
    principal_email = auto_field(validate=[Email(), Length(min=10)], data_key='principalEmail')
    username = auto_field(data_key='username')
    secondary_email = auto_field(data_key='secondaryEmail')
    password = fields.Str(load_only=True, validate=[Length(min=8, max=300)], data_key='password')
    password_confirmation = fields.Str(validate=[Length(min=8, max=300)], data_key='passwordConfirmation')
    avatar_url = auto_field(data_key='avatarUrl')
    current_theme = auto_field(default=0, validate=[Range(min=0)], data_key='currentTheme')
    admin = auto_field(data_key='admin'),
    active = auto_field(data_key='active')
    first_name = auto_field(data_key='firstName')
    last_name = auto_field(data_key='lastName')

    @validates_schema
    def validate_password_and_password_confirmation(self, data, **kwargs):
        if data.get("password", True) != data.get("password_confirmation"):
            raise ValidationError("password and confirm password must match")

    @validates_schema
    def validate_emails(self, data, **kwargs):
        if not (data.get("principal_email") is None and data.get("secondary_email") is None):
            if data.get("principal_email", '') == data.get("secondary_email", ''):
                raise ValidationError("principal email must be different than secondary email")


class ValidateUserSchema(UserSchema):
    class Meta:
        # unknown = EXCLUDE
        model = User
        load_instance = True
        exclude = ('current_theme',)


class ValidateUpdateUserSchema(SQLAlchemySchema):
    class Meta:
        unknown = EXCLUDE
        model = User

    id_ = fields.Integer(required=True, data_key="id", attribute='id')
    principal_email = auto_field(required=False)
    username = auto_field(required=False)
    secondary_email = auto_field(required=False)
    avatar_url = auto_field(required=False)
    current_theme = auto_field(required=False)
    admin = auto_field(required=False)
    active = auto_field(required=False, load_default=True, dump_default=True)
    first_name = auto_field(required=False)
    last_name = auto_field(required=False)

    @validates_schema
    def validate_emails(self, data, **kwargs):
        if not (data.get("principal_email") is None and data.get("secondary_email") is None):
            if data.get("principal_email", '') == data.get("secondary_email", ''):
                raise ValidationError("principal email must be different than secondary email")


class InputLoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class SuccessGetUserSchema(UserSchema):
    class Meta:
        exclude = ('password',)


class FailGetUserSchema(Fail):
    ...


class FailCreationUserSchema(Fail):
    message = fields.Str(load_default='Fail Creation User')


class FailLoginUserSchema(Fail):
    # errors = fields.Tuple(tuple_fields=(fields.String(),), required=True)
    message = fields.Str(load_default='Login Fail')


class SuccessLoginUserSchema(Schema):
    token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    message = fields.Str(dump_default='success', load_default='success')


class SuccessDeleteUserSchema(Success):
    deleted_id = fields.Integer(required=True)


class FailDeleteUserSchema(Fail):
    ...


class SuccessUpdateUserSchema(Schema):
    updated_id = fields.Integer(required=True)


class FailUpdateUserSchema(Fail):
    message = fields.Str(load_default='Update Fail', )
