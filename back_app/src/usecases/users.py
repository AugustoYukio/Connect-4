from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_header
from ..utils.users import create_user, authenticate, find_user, delete_user, update_user

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')


@bp_user.route('/<user_id>', methods=['GET'])
# @jwt_required()
def get(user_id):
    only_active = False
    return find_user(current_app, user_id, only_active)


@bp_user.route('/', methods=['POST'])
def create():
    return create_user(current_app, request.get_json())


@bp_user.route('/<user_id>', methods=['DELETE'])
def delete(user_id):
    force = True
    return delete_user(current_app, user_id, force_delete=force)


@bp_user.route('/', methods=['PUT'])
def udpate():
    force = True
    data = request.get_json()
    return update_user(current_app, data, force)


@bp_user.route('/login', methods=['POST'])
def login():
    return authenticate(request.get_json())


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
