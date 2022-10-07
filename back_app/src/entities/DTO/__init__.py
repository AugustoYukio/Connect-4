from flask_marshmallow.sqla import SQLAlchemySchema
from flask_marshmallow.fields import fields
from marshmallow import fields, validates, ValidationError, post_load
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

ma = Marshmallow()

