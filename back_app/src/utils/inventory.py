from back_app import Inventory
from ..entities.DTO import (
    ValidationError, validate_inventory_schema, validate_inventory_schema, success_create_inventory_schema,
    fail_creation_inventory_schema, success_get_inventory_schema, fail_get_inventory_schema,
    success_delete_inventory_schema, fail_delete_inventory_schema, success_update_inventory_schema,
    fail_update_inventory_schema
)


def delete_inventory_item(current_app, user_id, theme_id):
    pass


def find_inventory_item(theme_id, user_id):
    if not theme_id:
        return fail_get_inventory_schema.load({'errors': [{1: 'themeId must not be empty'}]})
    try:
        inventory = Inventory.query.get((user_id, theme_id,))
        if inventory is None:
            return fail_get_inventory_schema.dump(
                {'errors': {1: 'Not Found'}, 'message': f'Inventory.themeId: {theme_id} not found'}
            ), 200

        return success_get_inventory_schema.dump(inventory), 200
    except ValidationError as error:
        fail = fail_get_inventory_schema.load({'errors': [erro for erro in error.args], 'message': "Fail"})
        return fail, 301


def find_all_inventories_items_by_user_id(user_id, page=1, per_page=25):
    per_page = min(25, per_page)
    inventory = Inventory.query.where(
        Inventory.user_id.is_(user_id)
    ).order_by(Inventory.theme_id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return {
        'page': page,
        'perPage': per_page,
        'hasNext': inventory.has_next,
        'hasPrev': inventory.has_prev,
        'pageList': [inventory_page if inventory_page else '...' for inventory_page in inventory.iter_pages()],
        'count': inventory.total,
        'items': success_get_inventory_schema.dump(inventory.items, many=True)
    }


def get_all_inventories(user_id):
    inventory = Inventory.query.with_entities(Inventory.theme_id).where(Inventory.user_id.is_(user_id))
    return success_get_inventory_schema.dump(inventory, many=True)


def create_inventory_item(current_app, user_id, theme_id):
    with current_app.app_context() as ctx:
        ctx.app.db.session.add(Inventory(user_id=user_id, theme_id=theme_id))
        ctx.app.db.session.commit()
