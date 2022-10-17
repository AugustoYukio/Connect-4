from datetime import timedelta
from eventlet.websocket import BadRequest
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError
from sqlalchemy import select, delete, and_, or_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.testing import eq_

from ..entities.DTO import (fail_get_user_schema,
                            validate_user_schema, fail_creation_user_schema,
                            input_login_user_schema, fail_delete_user_schema,
                            fail_update_user_schema,
                            validate_update_user_schema, success_update_user_schema, success_delete_user_schema,
                            success_get_user_schema, success_login_user_schema
                            )
from ..entities.model.user import User
from .messages import MSG_INVALID_CREDENTIALS


def make_login_response(user: User) -> dict:
    acess_token = create_access_token(identity=user.id, expires_delta=timedelta(days=5))

    refresh_token = create_refresh_token(identity=user.id)
    return success_login_user_schema.load(
        {'token': acess_token, 'refresh_token': refresh_token, 'message': 'success'}
    )


def create_user(ctx_app, data):
    try:

        user = validate_user_schema.load(data=data)
        user.gen_hash()
    except ValidationError as error:
        # import ipdb;ipdb.set_trace()
        fail = fail_creation_user_schema.load({'errors': [erro for erro in error.args], 'message': "Fail Creation"})
        return jsonify(fail), 301
    except BadRequest as error:
        fail = fail_creation_user_schema.load(
            {'error': [{'description': error.description}], 'message': "Fail Creation"})
        return jsonify(fail), 400
    try:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.add(user)
            ctx.app.db.session.commit()
    except (IntegrityError,) as error:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.rollback()
            ctx.app.db.session.commit()

        fail = fail_creation_user_schema.load(
            {'errors': [{n_erro + 1: erro} for n_erro, erro in enumerate(error.orig.args)], 'message': "Fail Creation"}
        )
        return jsonify(fail), 500

    else:
        return jsonify(make_login_response(user)), 201


def authenticate(data):
    user = None
    try:
        # import ipdb;ipdb.set_trace()
        user_schema = input_login_user_schema.load(data=data)

    except ValidationError as error:
        return jsonify(error), 401

    # import ipdb;ipdb.set_trace()
    user = User.query.filter_by(username=user_schema.get('username')).first()

    if user and user.verify_password(user_schema.get('password')):
        return make_login_response(user)

    return jsonify({
        'message': MSG_INVALID_CREDENTIALS
    }), 401


def find_user(ctx_app, user_id, only_active=True):
    # import ipdb;ipdb.set_trace()
    if not user_id:
        return fail_get_user_schema.load({'errors': [{1: 'user_id must not be empty'}], 'message': "Fail"})
    try:
        clausule = User.id.is_(user_id)
        if only_active:
            clausule = (User.active.is_(True) & clausule)
        db_reponse = ctx_app.db.session.execute(
            select(User).where(clausule)
        ).first()
        if db_reponse is None:
            return fail_get_user_schema.dump(
                {'errors': [{1: 'Not Found'}], 'message': f'User id: {user_id} not found'}
            ), 200
        user = db_reponse[0]
        return success_get_user_schema.dump(user), 200
    except ValidationError as error:
        fail = fail_creation_user_schema.load({'errors': [erro for erro in error.args], 'message': "Fail Creation"})
        return fail, 301


def delete_user(ctx_app, user_id, force_delete=False):
    if not user_id:
        return fail_delete_user_schema.load(
            {'message': 'Fail Delete', 'errors': [{1: f"User id must not empty."}]}
        ), 404
    if not force_delete:
        resut_update = update_user(ctx_app, {'id': user_id, 'active': False})
        return success_delete_user_schema.load(
            {'data': f'affected rows: {resut_update}'}), 202
    try:
        affected_rows = ctx_app.db.session.execute(delete(User).where(User.id.is_(user_id)))
        if affected_rows.rowcount == 0:
            return fail_delete_user_schema.load(
                {'message': 'Fail Delete', 'errors': [{1: f"User id: {user_id} not found"}]}
            ), 404
        ctx_app.db.session.commit()
    except ValidationError as error:
        return fail_delete_user_schema.load(
            {'message': 'Fail Delete', 'errors': [erro for erro in error.args]}
        ), 400

    return success_delete_user_schema.load(
        {'data': f'affected rows: {affected_rows.rowcount}'}), 202


def update_user(ctx_app, data, force=False):
    if not data.get('id'):
        return fail_update_user_schema.load({'errors': [{1: f"User id must not empty."}]}), 404

    user = find_user(ctx_app, data.get('id'), False)
    try:
        valid_data = validate_update_user_schema.load(data)
    except ValidationError as error:
        return fail_update_user_schema.dump({'errors': [erro for erro in error.args]}), 400

    user_update = user[0] | valid_data
    try:
        affected_rows = ctx_app.db.session.execute(
            update(User).where(User.id.is_(user[0].get('id'))).values(**valid_data))
        if affected_rows.rowcount == 0:
            return fail_update_user_schema.load({'errors': [{1: f"User id: {data.get('id')} not found"}]}), 404
    except (IntegrityError,) as error:
        return fail_update_user_schema.load(
            {'errors': [{n_erro + 1: erro} for n_erro, erro in enumerate(error.orig.args)]}), 400
    else:
        ctx_app.db.session.commit()
    return success_update_user_schema.dump(user_update), 202
