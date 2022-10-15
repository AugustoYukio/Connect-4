from typing import Union
from marshmallow import Schema, fields


class Success(Schema):
    data = fields.Str(required=False)
    message = fields.Str(required=True)


class Fail(Schema):
    errors = fields.List(cls_or_instance=Union[fields.Dict], required=True)
    message = fields.Str(required=True)

