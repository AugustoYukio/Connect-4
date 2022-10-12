from typing import Union
from flask_marshmallow.sqla import SQLAlchemySchema
from flask_marshmallow.fields import fields
from marshmallow import fields, validates, ValidationError, post_load
from flask_marshmallow import Marshmallow, Schema
from marshmallow_sqlalchemy import auto_field
#from .. entities.model.user import User, Author, Book
from ..model.user import User, Author, Book


class AuthorSchema(SQLAlchemySchema):
    class Meta:
        model = Author
        load_instance = True  # Optional: deserialize to model instances

    id = auto_field()
    name = auto_field()
    books = auto_field()


class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True
        include_relationships = True

    id = auto_field()
    title = auto_field()
    author_id = auto_field()


class InputCreateUserSchema(SQLAlchemySchema):
    class Meta:
        # unknown = EXCLUDE
        model = User
        load_instance = True
        # include_fk = True

    principal_email = auto_field()
    username = auto_field()
    secondary_email = auto_field()
    password = auto_field()
    avatar_url = auto_field()
    default_theme = auto_field()
    admin = auto_field()
    active = auto_field()
    first_name = auto_field()
    last_name = auto_field()


class InputLoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class FailCreationUserSchema(Schema):
    errors = fields.List(cls_or_instance=Union[fields.Dict], required=True)
    message = fields.Str(default='Fail Creation User',  required=True)


class FailLoginUserSchema(Schema):
    errors = fields.Tuple(tuple_fields=(fields.String(),), required=True)
    message = fields.Str(default='Login Fail')


class SuccessLoginUserSchema(Schema):
    username = fields.Str(required=True)
    token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    message = fields.Str(required=True)