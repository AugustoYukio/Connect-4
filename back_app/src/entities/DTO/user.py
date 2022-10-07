from marshmallow_sqlalchemy import auto_field

from . import SQLAlchemySchema, fields
from back_app.src.entities.model.user import User, Author, Book


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

    # principal_email = fields.Str(required=True, dump_only=True)
    # username = fields.Str(required=True, dump_only=True)
    # secondary_email = fields.Str(required=True, dump_only=True)
    # password = fields.Str(required=True, dump_only=True)
    # avatar_url = fields.Str(dump_only=True)
    # default_theme = fields.Str(dump_only=True, required=False)
    # admin = fields.Boolean(dump_only=True, required=False)
    # active = fields.Boolean(dump_only=True, required=False)
    # first_name = fields.Str(dump_only=True, required=True)
    # last_name = fields.Str(dump_only=True, required=True)
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

class InputLoginUserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    username = fields.Str(required=True)
    password = fields.Str(required=True)


class OutputLoginUserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    username = fields.Str(required=True)
    token_jwt = fields.Str(required=False)
    refresh_token_jwt = fields.Str(required=False)
