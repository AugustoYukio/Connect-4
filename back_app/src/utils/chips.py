from . import *
from ..entities.DTO import (
    validate_chip_schema, fail_creation_chip_schema, fail_delete_chip_schema, success_delete_chip_schema,
    fail_update_chip_schema, success_update_chip_schema, fail_get_chip_schema, success_get_chip_schema
)
from ..entities.model.chip import Chip


def create_chip(ctx_app, data):
    try:
        chip = validate_chip_schema.load(data=data)

    except ValidationError as error:

        fail = fail_creation_chip_schema.load(
            {'errors': [erro for erro in error.args], 'message': "Fail Creation Chip"})
        return jsonify(fail), 301
    except BadRequest as error:
        fail = fail_creation_chip_schema.load(
            {'error': [{'description': error.description}], 'message': "Fail Creation Chip"})
        return jsonify(fail), 400
    try:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.add(chip)
            ctx.app.db.session.commit()
    except Exception as error:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.rollback()
            ctx.app.db.session.commit()

        fail = fail_creation_chip_schema.load(
            {'errors': [{n_erro + 1: erro} for n_erro, erro in enumerate(error.orig.args)],
             'message': "Fail Creation Chip"}
        )
        return jsonify(fail), 400

    else:
        return validate_chip_schema.dump(chip), 201


def delete_chip(ctx_app, chip_id):
    if not chip_id.strip():
        return fail_delete_chip_schema.load(
            {'message': 'Fail Delete', 'errors': {1: f"Chip id must not empty."}}
        ), 404

    try:
        affected_rows = ctx_app.db.session.execute(delete(Chip).where(Chip.id.is_(chip_id)))
        if affected_rows.rowcount == 0:
            return fail_delete_chip_schema.load(
                {'message': 'Fail Delete', 'errors': {1: f"Chip id: {chip_id} not found"}}
            ), 404
        ctx_app.db.session.commit()
    except ValidationError as error:
        return fail_delete_chip_schema.load(
            {'errors': {n_erro + 1: erro for n_erro, erro in enumerate(error.orig.args)}, 'message': 'Fail Delete'}
        ), 400

    return success_delete_chip_schema.load(
        {'data': f'affected rows: {affected_rows.rowcount}', 'message': 'success'}), 202


def update_chip(ctx_app, data):
    chip_id = data.pop('id', None)

    if chip_id is None:
        return fail_update_chip_schema.load({'errors': {1: f"Chip id must not empty."}}), 404

    try:
        valid_data = validate_chip_schema.dump(data)
    except ValidationError as error:
        return fail_update_chip_schema.dump(
            {'errors': {n_erro + 1: erro for n_erro, erro in enumerate(error.normalized_messages())}}
        ), 400
    stmt = update(Chip).where(Chip.id == chip_id).values(**valid_data)

    try:
        affected_rows = ctx_app.db.session.execute(stmt)
        if affected_rows.rowcount == 0:
            return fail_update_chip_schema.load({'errors': [{1: f"Chip id: {chip_id} not found"}]}), 404
    except (IntegrityError,) as error:
        return fail_update_chip_schema.load({'errors': {"IntegrityError": error.orig.args}}), 400
    else:
        ctx_app.db.session.commit()
    return success_update_chip_schema.load({'updated_id': chip_id}), 202


def find_chip(chip_id: str):
    if not chip_id:
        return fail_get_chip_schema.load({'errors': [{1: 'chip_id must not be empty'}]})
    try:
        found_chip = Chip.query.get(chip_id)
        if found_chip is None:
            return fail_get_chip_schema.dump(
                {'errors': {1: 'Not Found'}, 'message': f'Chip id: {chip_id} not found'}
            ), 200

        return success_get_chip_schema.dump(found_chip), 200
    except ValidationError as error:
        fail = fail_get_chip_schema.load({'errors': [erro for erro in error.args], 'message': "Fail"})
        return fail, 301


def find_chips(ctx_app, chip_ids: []):
    if not chip_ids:
        return fail_get_chip_schema.load({'errors': [{1: 'chip_ids must not be empty'}]})
    try:
        clausule = Chip.id.in_(chip_ids)
        db_reponse = ctx_app.db.session.execute(select(Chip).where(clausule)).all()
        if not db_reponse:
            return fail_get_chip_schema.dump(
                {'errors': [{1: 'Not Found'}], 'message': f'Chip ids: {chip_ids} not found'}
            )
        found_chips = db_reponse[0]
        return {'message': 'success', 'result': success_get_chip_schema.dump(found_chips, many=True)}
    except ValidationError as error:
        fail = fail_get_chip_schema.load({'errors': [erro for erro in error.args], 'message': "Fail"})
        return fail
