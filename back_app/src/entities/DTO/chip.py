from typing import Union
from marshmallow import Schema, fields
from flask_marshmallow.sqla import SQLAlchemySchema
from .base_schemas import Success, Fail
from ..model.chip import Chip


class ChipSchema(SQLAlchemySchema):
    class Meta:
        # unknown = EXCLUDE
        model = Chip
        load_instance = True

    id_ = fields.Integer(required=True, data_key="id", attribute='id', dump_only=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)


class ValidateChipSchema(ChipSchema):
    ...


class FailCreationChipSchema(Fail):
    ...


class SuccessCreateChipSchema(Success):
    ...


class SuccessDeleteChipSchema(Success):
    ...


class FailDeleteChipSchema(Fail):
    ...


class SuccessGetChipSchema(ValidateChipSchema):
    ...


class FailGetChipSchema(Fail):
    ...


class SuccessUpdateChipSchema(Success):
    updated_id = fields.Integer(required=True)


class FailUpdateChipSchema(Fail):
    ...


