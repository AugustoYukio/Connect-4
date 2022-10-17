from eventlet.websocket import BadRequest
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.sql import Delete, Select, update

from ..entities.DTO import validate_chip_schema,fail_creation_chip_schema, fail_delete_chip_schema, \
    success_delete_chip_schema, fail_update_chip_schema, success_update_chip_schema
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
        return jsonify(validate_chip_schema.dump(chip)), 201


def delete_chip(ctx_app, data):
    _id = data.get('id')
    if _id is None:
        return fail_delete_chip_schema.load(
            {'message': 'Fail Delete', 'errors': [{1: f"Chip id must not empty."}]}
        ), 404

    try:
        affected_rows = ctx_app.db.session.execute(Delete(Chip).where(Chip.id.is_(_id)))
        if affected_rows.rowcount == 0:
            return fail_delete_chip_schema.load(
                {'message': 'Fail Delete', 'errors': [{1: f"Chip id: {_id} not found"}]}
            ), 404
        ctx_app.db.session.commit()
    except ValidationError as error:
        return fail_delete_chip_schema.load(
            {'message': 'Fail Delete', 'errors': [erro for erro in error.args]}
        ), 400

    return success_delete_chip_schema.load({'data': f'affected rows: {affected_rows.rowcount}', 'message': 'success'}), 202


def update_chip(ctx_app, data, _id):
    found_chip = Chip.query.where(Chip.id == _id).first()
    if found_chip is None:
        return fail_update_chip_schema.load(
            {'errors': [{1: "Chip id must not be empty and must exist."}], 'message': "Fail Update Chip"})
    try:
        validate_chip_schema.load(data=data)
    except ValidationError as error:
        fail = fail_update_chip_schema.load(
            {'errors': [erro for erro in error.args], 'message': "Fail Update Chip"})
        return jsonify(fail), 301

    ctx_app.db.session.execute(update(Chip).where(Chip.id == found_chip.id).values(**data))
    ctx_app.db.session.commit()
    return success_update_chip_schema.load({'message': "Success Update Chip"}), 200
