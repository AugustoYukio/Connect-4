from typing import Union
from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema
from marshmallow import fields

from .base_schemas import Fail
from .chip import ChipsSchema
from ..model.theme import Theme


class ThemeSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        # unknown = EXCLUDE
        model = Theme
        load_instance = True
        # include_fk = True
        load_relationships = True

    name = auto_field(required=True, )
    price = auto_field(required=True)
    chip1_id = fields.Nested(ChipsSchema)
    chip2_id = fields.Nested(ChipsSchema)
    board_id = auto_field(required=True)


class ValidateThemeSchema(ThemeSchema):
    ...


class FailCreationThemeSchema(Fail):
    message = fields.Str(default='Fail Creation User', required=True)
