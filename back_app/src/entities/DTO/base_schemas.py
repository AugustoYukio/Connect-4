from typing import Union
from marshmallow import Schema, fields


class Success(Schema):
    data = fields.Str(required=False)
    message = fields.Str(dump_default='success', load_default='success')


class Fail(Schema):
    errors = fields.Dict(cls_or_instance=fields.Str, required=True)
    message = fields.Str(dump_default='fail', load_default='fail')

