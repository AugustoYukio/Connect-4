from marshmallow import fields
from flask_marshmallow.sqla import SQLAlchemySchema
from .base_schemas import Success, Fail
from ..model.board import Board


class BoardSchema(SQLAlchemySchema):
    class Meta:
        # unknown = EXCLUDE
        model = Board
        load_instance = True

    id_ = fields.Integer(required=True, data_key="id", attribute='id', dump_only=True)
    name = fields.Str(required=True, data_key="name")
    url = fields.Str(required=True, data_key="url")


class ValidateBoardSchema(BoardSchema):
    ...


class SuccessCreateBoardSchema(Success):
    ...


class FailCreationBoardSchema(Fail):
    ...


class SuccessGetBoardSchema(ValidateBoardSchema):
    ...


class FailGetBoardSchema(Fail):
    ...


class SuccessDeleteBoardSchema(Success):
    ...


class FailDeleteBoardSchema(Fail):
    ...


class SuccessUpdateBoardSchema(Success):
    updated_id = fields.Integer(required=True)


class FailUpdateBoardSchema(Fail):
    ...
