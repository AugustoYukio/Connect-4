from . import (Blueprint, get_jwt_identity, request, current_app, admin_required, owner_required)
from ..utils.inventory import (find_inventory_item, delete_inventory_item, find_all_inventories_items_by_user_id,
                               create_inventory_item, )

bp_inventory = Blueprint('bp_inventory', __name__, url_prefix='/inventory')


@bp_inventory.route('/', methods=['POST'])
@admin_required()
def create(user_id=None, theme_id=None):
    data = request.get_json()
    return create_inventory_item(current_app, user_id, theme_id)


@bp_inventory.route('/<theme_id>', methods=['GET'])
@owner_required()
def get(user_id=None, theme_id=None):
    return find_inventory_item(theme_id, user_id)


@bp_inventory.route('/', methods=['GET'])
@owner_required()
def get_all(user_id):
    return find_all_inventories_items_by_user_id(user_id)


# @bp_inventory.route('/<user_id>/<theme_id>', methods=['DELETE'])
# @admin_required()
# def delete(user_id, theme_id):
#     return delete_inventory_item(current_app, user_id, theme_id)
