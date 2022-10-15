from datetime import timedelta
from eventlet.websocket import BadRequest
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError
from ..entities.DTO import (
    validate_user_schema, fail_creation_user_schema, success_login_user_chema, input_login_user_schema,
)
from ..entities.model.user import User
from .messages import MSG_INVALID_CREDENTIALS


def make_login_response(user: User) -> dict:
    acess_token = create_access_token(identity=user.id, expires_delta=timedelta(days=5))

    refresh_token = create_refresh_token(identity=user.id)
    return success_login_user_chema.load(
        {'token': acess_token, 'refresh_token': refresh_token, 'message': 'success'}
    )


def create_user(ctx_app, data):
    try:
        # import ipdb;ipdb.set_trace()
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
    except Exception as error:
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
