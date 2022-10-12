import ipdb
from datetime import timedelta, datetime

import jwt
from flask import Blueprint, request, jsonify, current_app, redirect, abort
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity, \
    verify_jwt_in_request, get_jwt_header
from flask_marshmallow.sqla import SQLAlchemySchema
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from ..entities.DTO import (input_login_user_schema, fail_creation_user_schema, input_create_user_schema,
                            InputLoginUserSchema, FailCreationUserSchema, FailLoginUserSchema, SuccessLoginUserSchema,
                            success_login_user_chema
                            )

from ..entities.model.user import User

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')


@bp_user.route('/ping', methods=['GET'])
def teste():
    return 'OK'


@bp_user.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return user_id


def make_login_response(user: User) -> dict:
    acess_token = create_access_token(
        identity=user.id, expires_delta=timedelta(days=25), additional_headers={'username': user.username}
    )

    refresh_token = create_refresh_token(identity=user.id)
    return success_login_user_chema.load(
        {'username': user.username, 'token': acess_token, 'refresh_token': refresh_token, 'message': 'success'}
    )


@bp_user.route('/create', methods=['POST'])
def register():
    try:
        # import ipdb;ipdb.set_trace()
        user = input_create_user_schema.load(data=request.json)
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
        with current_app.app_context() as ctx:
            ctx.app.db.session.add(user)
            ctx.app.db.session.commit()
    except Exception as error:
        with current_app.app_context() as ctx:
            ctx.app.db.session.rollback()
            ctx.app.db.session.commit()

        fail = fail_creation_user_schema.load(
            {'errors': [{n_erro + 1: erro} for n_erro, erro in enumerate(error.orig.args)], 'message': "Fail Creation"}
        )
        return jsonify(fail), 500

    else:
        return jsonify(make_login_response(user)), 201


@bp_user.route('/login', methods=['POST'])
def login():
    try:
        user_data_login = input_login_user_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error), 401

    # import ipdb;ipdb.set_trace()
    user = User.query.filter_by(username=user_data_login.get('username')).first()

    if user and user.verify_password(user_data_login.get('password'), ):
        return make_login_response(user)

    return jsonify({
        'message': r'Invalid login and/or password'
    }), 401


@bp_user.route('/proibido', methods=['GET'])
@jwt_required()
def rota_autenticada():
    current_user = get_jwt_header().get('username')
    return jsonify({'res': f'Você está logado: {current_user}'})


@bp_user.route('/proibidao', methods=['GET'])
@jwt_required()
def rota_autenticada_e_admins():
    current_user = get_jwt_header().get('username')
    return jsonify({'res': f'Você está logado e é um administrador. {current_user}'})
