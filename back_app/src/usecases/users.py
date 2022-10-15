from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_header
from ..utils.users import create_user, authenticate

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')


@bp_user.route('/ping', methods=['GET'])
def teste():
    return 'OK'


@bp_user.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return user_id


@bp_user.route('/create', methods=['POST'])
def register():
    return create_user(current_app, request.get_json())


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
