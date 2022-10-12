from . user import (
     InputCreateUserSchema, InputLoginUserSchema, FailCreationUserSchema, FailLoginUserSchema,
     SuccessLoginUserSchema, Marshmallow
     )

input_create_user_schema = InputCreateUserSchema()
input_login_user_schema = InputLoginUserSchema()
fail_creation_user_schema = FailCreationUserSchema()
success_login_user_chema = SuccessLoginUserSchema()
ma = Marshmallow()

