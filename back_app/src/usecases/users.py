import os
from datetime import timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_refresh_token, create_access_token
from marshmallow import ValidationError

from ..entities.DTO.user import InputLoginUserSchema, CreatUserSchema
from ..entities.model.user import User

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite://' + os.path.join(basedir, 'app.db')


@bp_user.route('/ping', methods=['GET'])
def teste():
    return 'OK'


user_schema_create = CreatUserSchema()


@bp_user.route('/<id:str>', methods=['GET'])
def get_user(id):
    ...


@bp_user.route('/create', methods=['POST'])
def register():
    try:
        user = CreatUserSchema().load(request.json)

    except ValidationError as error:
        return jsonify(error), 401

    user.gen_hash()

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return user.jsonify(user), 201


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
