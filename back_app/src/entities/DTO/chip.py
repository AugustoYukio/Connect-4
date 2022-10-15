from typing import Union
from marshmallow import Schema, fields
from flask_marshmallow.sqla import SQLAlchemySchema
from .base_schemas import Success, Fail
from ..model.chip import Chip


class ChipsSchema(SQLAlchemySchema):
    class Meta:
        # unknown = EXCLUDE
        model = Chip
        load_instance = True

    name = fields.Str(required=True)
    url = fields.Str(required=True)


class ValidateChipSchema(ChipsSchema):
    ...


class FailCreationChipSchema(Fail):
    ...


class SuccessCreateChipSchema(Success):
    ...


class SuccessDeleteChipSchema(Success):
    ...


class FailDeleteChipSchema(Fail):
    ...


class SuccessUpdateChipSchema(Success):
    ...


class FailUpdateChipSchema(Fail):
    ...
