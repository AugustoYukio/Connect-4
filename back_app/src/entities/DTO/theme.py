from flask_marshmallow.sqla import auto_field, SQLAlchemyAutoSchema
from marshmallow import fields
from .base_schemas import Fail, Success
from ..model.theme import Theme


class ThemeSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        # unknown = EXCLUDE
        model = Theme
        load_instance = True
        # include_fk = True
        load_relationships = True

    name = auto_field(required=True, data_key='name')
    price = auto_field(required=True, data_key='price')
    chip1_id = auto_field(required=True, data_key='chip1Id')
    chip2_id = fields.Integer(required=True, data_key='chip2Id')
    board_id = fields.Integer(required=True, data_key='boardId')
    image = fields.Str(required=True, data_key='themeImage')


class ValidateThemeSchema(ThemeSchema):
    ...


class FailCreationThemeSchema(Fail):
    message = fields.Str(default='Fail Creation Theme')


class SuccessCreateThemeSchema(Success):
    ...


class SuccessGetThemeSchema(ValidateThemeSchema):
    ...


class FailGetThemeSchema(Fail):
    ...


class SuccessDeleteThemeSchema(Success):
    ...


class FailDeleteThemeSchema(Fail):
    ...


class SuccessUpdateThemeSchema(Success):
    updated_id = fields.Integer(required=True)


class FailUpdateThemeSchema(Fail):
    ...
