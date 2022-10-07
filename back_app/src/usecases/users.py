from datetime import timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_refresh_token, create_access_token
from marshmallow import ValidationError
from ..entities.DTO.user import (
    InputLoginUserSchema, InputCreateUserSchema, InputLoginUserSchema, OutputLoginUserSchema, AuthorSchema, BookSchema
)
from ..entities.model.user import User, Author, Book

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')


@bp_user.route('/ping', methods=['GET'])
def teste():
    return 'OK'


@bp_user.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return user_id


@bp_user.route('/create', methods=['POST'])
def register():
    try:
        input_user = InputCreateUserSchema()
        user = input_user.load(data=request.json)
        user.gen_hash()
    except ValidationError as error:
        return jsonify(error), 401

    try:
        with current_app.app_context() as ctx:
            ctx.app.db.session.add(user)
            ctx.app.db.session.commit()
    except Exception as error:
        return jsonify(error), 401
    return jsonify(user), 201


@bp_user.route('/login', methods=['POST'])
def login():
    user, error = InputLoginUserSchema().load(request.json)

    if error:
        return jsonify(error), 401

    user = User.query.filter_by(username=user.username).first()

    if user and user.verify_password(request.json['password']):
        acess_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(minutes=150),
            additional_headers=user.admin
        )
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'acess_token': acess_token,
            'refresh_token': refresh_token,
            'message': 'sucess'
        }), 200

    return jsonify({
        'message': r'Invalid login and/or password'
    }), 401
