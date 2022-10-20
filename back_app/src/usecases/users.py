from flask_jwt_extended import get_jwt_identity, get_jwt
from . import (Blueprint, request, current_app, jwt_required, jsonify, resp_notallowed_user)
from back_app.src.utils.users import create_user, authenticate, find_user, delete_user, update_user


bp_user = Blueprint('bp_user', __name__, url_prefix='/user')


@bp_user.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get(user_id):
    if get_jwt_identity() == user_id:
        return jsonify(find_user(current_app, user_id, True))

    if get_jwt().get('is_admin'):
        return jsonify(find_user(current_app, user_id, False))

    return resp_notallowed_user()


@bp_user.route('/', methods=['POST'])
def create():
    return jsonify(create_user(current_app, request.get_json()))


@bp_user.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete(user_id):
    if get_jwt_identity() == user_id:
        return jsonify(delete_user(current_app, user_id, force_delete=False))

    if get_jwt().get('is_admin'):
        return jsonify(delete_user(current_app, user_id, force_delete=True))

    return resp_notallowed_user()


@bp_user.route('/', methods=['PUT'])
@jwt_required()
def udpate():
    data = request.get_json()
    if get_jwt_identity() == data.get('id'):
        return jsonify(update_user(current_app, data))

    if get_jwt().get('is_admin'):
        return jsonify(update_user(current_app, data))

    return resp_notallowed_user()


@bp_user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authenticate(data)
