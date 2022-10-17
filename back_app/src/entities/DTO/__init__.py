from flask_marshmallow import Marshmallow

from .chip import (ValidateChipSchema, FailCreationChipSchema, FailDeleteChipSchema, SuccessCreateChipSchema,
                   SuccessDeleteChipSchema, SuccessUpdateChipSchema, FailUpdateChipSchema, )
from .user import (
    ValidateUserSchema, InputLoginUserSchema, FailCreationUserSchema, FailLoginUserSchema,
    SuccessLoginUserSchema, SuccessGetUserSchema, FailGetUserSchema, SuccessDeleteUserSchema, FailDeleteUserSchema,
    SuccessUpdateUserSchema, FailUpdateUserSchema, ValidateUpdateUserSchema
)
from .theme import (ValidateThemeSchema, FailCreationThemeSchema, )

# USER SCHEMAS
validate_user_schema = ValidateUserSchema()
input_login_user_schema = InputLoginUserSchema()
fail_creation_user_schema = FailCreationUserSchema()
success_login_user_chema = SuccessLoginUserSchema()
success_get_user_chema = SuccessGetUserSchema()
fail_get_user_schema = FailGetUserSchema()
success_delete_user_chema = SuccessDeleteUserSchema()
fail_delete_user_schema = FailDeleteUserSchema()
validate_update_user_chema = ValidateUpdateUserSchema()
success_update_user_chema = SuccessUpdateUserSchema()
fail_update_user_schema = FailUpdateUserSchema()

# CHIP SCHEMAS
validate_chip_schema = ValidateChipSchema()
success_create_chip_schema = SuccessCreateChipSchema()
fail_creation_chip_schema = FailCreationChipSchema()

success_delete_chip_schema = SuccessDeleteChipSchema()
fail_delete_chip_schema = FailDeleteChipSchema()

success_update_chip_schema = SuccessUpdateChipSchema()
fail_update_chip_schema = FailUpdateChipSchema()

# THEME SCHEMAS
validate_theme_schema = ValidateThemeSchema()
fail_creation_theme_schema = FailCreationThemeSchema()

ma = Marshmallow()
