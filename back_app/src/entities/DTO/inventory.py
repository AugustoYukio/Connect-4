from marshmallow import fields
from flask_marshmallow.sqla import SQLAlchemySchema
from .base_schemas import Success, Fail
from ..model.inventory import Inventory


class InventorySchema(SQLAlchemySchema):
    class Meta:
        # unknown = EXCLUDE
        model = Inventory
        load_instance = True

    user_id = fields.Integer(required=True, data_key="userId")
    theme_id = fields.Integer(required=True, data_key="themeId")


class ValidateInventorySchema(InventorySchema):
    ...


class SuccessCreateInventorySchema(Success):
    ...


class FailCreationInventorySchema(Fail):
    ...


class SuccessGetInventorySchema(ValidateInventorySchema):
    ...


class FailGetInventorySchema(Fail):
    ...


class SuccessDeleteInventorySchema(Success):
    ...


class FailDeleteInventorySchema(Fail):
    ...


class SuccessUpdateInventorySchema(Success):
    updated_id = fields.Integer(required=True)


class FailUpdateInventorySchema(Fail):
    ...


