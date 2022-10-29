from . import *
from .chips import find_chip, find_chips
from .inventory import find_all_inventories_items_by_user_id, get_all_inventories
from ..entities.DTO import (validate_theme_schema, fail_creation_theme_schema, fail_delete_theme_schema,
                            success_delete_theme_schema, fail_update_theme_schema, success_update_theme_schema,
                            fail_get_theme_schema, success_get_theme_schema, validate_chip_schema)
from ..entities.model.chip import Chip
from ..entities.model.theme import Theme


def create_theme(ctx_app, data):
    try:
        # validate_chip_schema.load()
        #        chips = find_chips(ctx_app, [data.get('chip1_id'), data.get('chip2_id')])
        #        if chips.get('errors') is not None:
        #            raise ValidationError(chips)

        theme = validate_theme_schema.load(data=data)

    except ValidationError as error:
        return fail_creation_theme_schema.dump({'errors': error.normalized_messages()})
    try:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.add(theme)
            ctx.app.db.session.commit()
    except IntegrityError as error:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.rollback()
        return fail_creation_theme_schema.load(
            {'errors': {"IntegrityError": error.orig.args}, 'message': "Fail Creation Theme"}
        ), 400
    else:
        return validate_theme_schema.load(theme), 201


def delete_theme(ctx_app, theme_id):
    if not theme_id.strip():
        return fail_delete_theme_schema.load(
            {'message': 'Fail Delete', 'errors': [{1: f"Theme id must not empty."}]}
        ), 404

    try:
        affected_rows = ctx_app.db.session.execute(delete(Theme).where(Theme.id.is_(theme_id)))
        if affected_rows.rowcount == 0:
            return fail_delete_theme_schema.load(
                {'message': 'Fail Delete', 'errors': [{1: f"Theme id: {theme_id} not found"}]}
            ), 404
        ctx_app.db.session.commit()
    except ValidationError as error:
        return fail_delete_theme_schema.load(
            {'message': 'Fail Delete', 'errors': [erro for erro in error.args]}
        ), 400

    return success_delete_theme_schema.load(
        {'data': f'affected rows: {affected_rows.rowcount}', 'message': 'success'}), 202


def update_theme(ctx_app, data):
    theme_id = data.pop('id', None)

    if theme_id is None:
        return fail_update_theme_schema.load({'errors': [{1: f"Theme id must not empty."}]}), 404
    try:
        valid_data = validate_theme_schema.dump(data)
    except ValidationError as error:
        return fail_update_theme_schema.dump({'errors': [erro for erro in error.args]}), 400

    try:
        stmt = update(Theme).where(Theme.id == theme_id).values(**valid_data)
        affected_rows = ctx_app.db.session.execute(stmt)
        if affected_rows.rowcount == 0:
            return fail_update_theme_schema.load({'errors': [{1: f"Theme id: {theme_id} not found"}]}), 404
    except (IntegrityError,) as error:
        return fail_update_theme_schema.load({'errors': {"IntegrityError": error.orig.args}}), 400
    else:
        ctx_app.db.session.commit()
    return success_update_theme_schema.dump({'updated_id': theme_id}), 202


def find_theme(theme_id: str):
    if not theme_id:
        return fail_get_theme_schema.load({'errors': [{1: 'theme_id must not be empty'}]})
    try:
        theme = Theme.query.get(theme_id)
        if theme is None:
            return fail_get_theme_schema.dump(
                {'errors': {1: 'Not Found'}, 'message': f'Theme id: {theme_id} not found'}
            ), 200

        return success_get_theme_schema.dump(theme), 200
    except ValidationError as error:
        fail = fail_get_theme_schema.load({'errors': [erro for erro in error.args], 'message': "Fail Creation"})
        return fail, 301


def find_themes_by_user(user_id, page=1, per_page=25):
    user_inventory_items = get_all_inventories(user_id)
    per_page = min(25, per_page)
    theme_paginate = Theme.query.order_by(Theme.name.desc()).paginate(page=page, per_page=per_page, error_out=False)

    items = success_get_theme_schema.dump(theme_paginate.items, many=True)
    ids_for_themes_user_owner = [inventory_item['themeId'] for inventory_item in user_inventory_items]


    for item in items:
        item["status"] = "unavailable" if item['id'] in ids_for_themes_user_owner else "available"

    return {
        'page': page,
        'perPage': per_page,
        'hasNext': theme_paginate.has_next,
        'hasPrev': theme_paginate.has_prev,
        'pageList': [inventory_page if inventory_page else '...' for inventory_page in theme_paginate.iter_pages()],
        'count': theme_paginate.total,
        'items': items
        }
