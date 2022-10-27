from . import *
from ..entities.DTO import (
    validate_board_schema, fail_creation_board_schema, fail_delete_board_schema, fail_update_board_schema,
    fail_get_board_schema, success_get_board_schema, success_update_board_schema, success_delete_board_schema
)
from ..entities.model.board import Board


def create_board(ctx_app, data):
    try:
        board = validate_board_schema.load(data=data)
    except ValidationError as error:
        fail = fail_creation_board_schema.load({'errors': error.normalized_messages()})
        return jsonify(fail), 301
    try:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.add(board)
            ctx.app.db.session.commit()
    except Exception as error:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.rollback()
            ctx.app.db.session.commit()

        fail = fail_creation_board_schema.load(
            {'errors': [{n_erro + 1: erro} for n_erro, erro in enumerate(error.orig.args)],
             'message': "Fail Creation Board"}
        )
        return fail, 400

    else:
        return validate_board_schema.dump(board), 201


def delete_board(ctx_app, board_id):

    if not board_id:
        return fail_delete_board_schema.load(
            {'message': 'Fail Delete', 'errors': {1: f"Board id must not empty."}}), 404

    try:
        affected_rows = ctx_app.db.session.execute(delete(Board).where(Board.id.is_(board_id)))
        if affected_rows.rowcount == 0:
            return fail_delete_board_schema.load(
                {'message': 'Fail Delete', 'errors': {1: f"Board id: {board_id} not found"}}
            ), 404
        ctx_app.db.session.commit()
    except ValidationError as error:
        return fail_delete_board_schema.load(
            {'message': 'Fail Delete', 'errors': error.normalized_messages()}
        ), 400

    return success_delete_board_schema.load(
        {'data': f'affected rows: {affected_rows.rowcount}', 'message': 'success'}), 202


def update_board(ctx_app, data):
    board_id = data.pop('id', None)

    if board_id is None:
        return fail_update_board_schema.load({'errors': {1: f"Board id must not empty."}}), 404

    try:
        valid_data = validate_board_schema.dump(data)
    except ValidationError as error:
        return fail_update_board_schema.dump({'errors': error.normalized_messages()}), 400

    try:
        stmt = update(Board).where(Board.id == board_id).values(**valid_data)
        affected_rows = ctx_app.db.session.execute(stmt)
        if affected_rows.rowcount == 0:
            return fail_update_board_schema.load({'errors': {1: f"Board id: {board_id} not found"}}), 404
    except (IntegrityError,) as error:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.rollback()
        return fail_creation_board_schema.load({'errors': {"IntegrityError": error.orig.args}}), 400
    else:
        ctx_app.db.session.commit()
    return success_update_board_schema.dump({'updated_id': board_id}), 202


def find_board(board_id: str):
    if not board_id.strip():
        return fail_get_board_schema.load({'errors': {1: 'board_id must not be empty'}})
    try:
        board = Board.query.get(board_id)
        if board is None:
            return fail_get_board_schema.dump(
                {'errors': {1: 'Not Found'}, 'message': f'Board id: {board_id} not found'}
            ), 200
        return success_get_board_schema.dump(board), 200
    except ValidationError as error:
        fail = fail_get_board_schema.load({'errors': error.normalized_messages(), 'message': "Fail Creation"})
        return fail, 301
