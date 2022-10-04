from marshmallow import fields, validates, ValidationError, post_load
from flask_marshmallow import Marshmallow

ma = Marshmallow()


def configure(app):
    ma.init_app(app)
