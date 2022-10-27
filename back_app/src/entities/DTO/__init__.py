from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from .board import (ValidateBoardSchema, SuccessCreateBoardSchema, FailCreationBoardSchema, SuccessGetBoardSchema,
                    SuccessDeleteBoardSchema, FailGetBoardSchema, FailDeleteBoardSchema, FailUpdateBoardSchema,
                    SuccessUpdateBoardSchema, )
from .chip import (
    ValidateChipSchema, FailCreationChipSchema, FailDeleteChipSchema, SuccessCreateChipSchema,
    SuccessDeleteChipSchema, SuccessUpdateChipSchema, FailUpdateChipSchema, FailGetChipSchema,SuccessGetChipSchema
                   )
from .inventory import (
    ValidateInventorySchema, SuccessCreateInventorySchema, FailCreationInventorySchema, SuccessGetInventorySchema,
    FailGetInventorySchema, SuccessDeleteInventorySchema, FailDeleteInventorySchema, SuccessUpdateInventorySchema,
    FailUpdateInventorySchema
)

from .user import (
    ValidateUserSchema, InputLoginUserSchema, FailCreationUserSchema, FailLoginUserSchema,
    SuccessLoginUserSchema, SuccessGetUserSchema, FailGetUserSchema, SuccessDeleteUserSchema, FailDeleteUserSchema,
    SuccessUpdateUserSchema, FailUpdateUserSchema, ValidateUpdateUserSchema
)
from .theme import (ValidateThemeSchema, FailCreationThemeSchema, SuccessCreateThemeSchema, SuccessGetThemeSchema,
                    FailGetThemeSchema, SuccessUpdateThemeSchema, FailDeleteThemeSchema, SuccessDeleteThemeSchema,
                    FailUpdateThemeSchema, )

# USER SCHEMAS
validate_user_schema = ValidateUserSchema()
input_login_user_schema = InputLoginUserSchema()
fail_creation_user_schema = FailCreationUserSchema()
success_login_user_schema = SuccessLoginUserSchema()
success_get_user_schema = SuccessGetUserSchema()
fail_get_user_schema = FailGetUserSchema()
success_delete_user_schema = SuccessDeleteUserSchema()
fail_delete_user_schema = FailDeleteUserSchema()
validate_update_user_schema = ValidateUpdateUserSchema()
success_update_user_schema = SuccessUpdateUserSchema()
fail_update_user_schema = FailUpdateUserSchema()

# CHIP SCHEMAS
validate_chip_schema = ValidateChipSchema()
success_create_chip_schema = SuccessCreateChipSchema()
fail_creation_chip_schema = FailCreationChipSchema()
success_get_chip_schema = SuccessGetChipSchema()
fail_get_chip_schema = FailGetChipSchema()
success_delete_chip_schema = SuccessDeleteChipSchema()
fail_delete_chip_schema = FailDeleteChipSchema()
success_update_chip_schema = SuccessUpdateChipSchema()
fail_update_chip_schema = FailUpdateChipSchema()

# BOARD SCHEMAS
validate_board_schema = ValidateBoardSchema()
success_create_board_schema = SuccessCreateBoardSchema()
fail_creation_board_schema = FailCreationBoardSchema()
success_get_board_schema = SuccessGetBoardSchema()
fail_get_board_schema = FailGetBoardSchema()
success_delete_board_schema = SuccessDeleteBoardSchema()
fail_delete_board_schema = FailDeleteBoardSchema()
success_update_board_schema = SuccessUpdateBoardSchema()
fail_update_board_schema = FailUpdateBoardSchema()

# THEME SCHEMAS
validate_theme_schema = ValidateThemeSchema()
success_create_theme_schema = SuccessCreateThemeSchema()
fail_creation_theme_schema = FailCreationThemeSchema()
success_get_theme_schema = SuccessGetThemeSchema()
fail_get_theme_schema = FailGetThemeSchema()
success_delete_theme_schema = SuccessDeleteThemeSchema()
fail_delete_theme_schema = FailDeleteThemeSchema()
success_update_theme_schema = SuccessUpdateThemeSchema()
fail_update_theme_schema = FailUpdateThemeSchema()

# INVENTORY SCHEMAS

validate_inventory_schema = ValidateInventorySchema()
success_create_inventory_schema = SuccessCreateInventorySchema()
fail_creation_inventory_schema = FailCreationInventorySchema()
success_get_inventory_schema = SuccessGetInventorySchema()
fail_get_inventory_schema = FailGetInventorySchema()
success_delete_inventory_schema = SuccessDeleteInventorySchema()
fail_delete_inventory_schema = FailDeleteInventorySchema()
success_update_inventory_schema = SuccessUpdateInventorySchema()
fail_update_inventory_schema = FailUpdateInventorySchema()
ma = Marshmallow()
