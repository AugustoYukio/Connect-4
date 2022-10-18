from flask_marshmallow.sqla import auto_field, SQLAlchemyAutoSchema
from marshmallow import fields
from .base_schemas import Fail, Success
from .chip import ChipSchema
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
    chip1_id = auto_field(required=True)
    chip2_id = auto_field(required=True)
    board_id = auto_field(required=True)


class ValidateThemeSchema(ThemeSchema):
    ...


class FailCreationThemeSchema(Fail):
    message = fields.Str(default='Fail Creation User', required=True)


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


class SuccessUpdateThemeSchema(ValidateThemeSchema):
    ...


class FailUpdateThemeSchema(Fail):
    ...
