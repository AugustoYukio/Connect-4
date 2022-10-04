from . import ma, fields, post_load
from back_app.src.entities.model.user import User


class CreatUserSchema(ma.Schema):
    class Meta:
        model = User

    # def __load__(self, data):
    # super().load(data)

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)

    #
    username = fields.Str(required=True)
    # principal_email = fields.Str(required=True)
    # secondary_email = fields.Str(required=True)
    # password = fields.Str(required=True)
    avatar_url = fields.Str()
    default_theme = fields.Str()


class InputLoginUserSchema(ma.Schema):
    class Meta:
        model = User

    username = fields.Str(required=True)
    password = fields.Str(required=True)


class OutputLoginUserSchema(ma.Schema):
    class Meta:
        model = User

    username = fields.Str(required=True)
    token_jwt = fields.Str(required=False)
    refresh_token_jwt = fields.Str(required=False)

# CreatUserSchema()
# Input_Users_schema = InputUserSchema(many=True)
