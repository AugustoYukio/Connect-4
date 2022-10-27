from . import (Blueprint, request, current_app, jwt_required, jsonify, get_jwt_identity, get_jwt, resp_notallowed_user)
from ..utils.users import create_user, authenticate, find_user, delete_user, update_user, get_count_of_admin_users

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')


@bp_user.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get(user_id):
    only_active = True
    is_admin = get_jwt().get('is_admin')
    if is_admin:
        only_active = False
    elif get_jwt_identity() != user_id:
        return resp_notallowed_user()
    return jsonify(find_user(user_id, only_active))


@bp_user.route('/', methods=['POST'])
def create():
    return jsonify(create_user(current_app, request.get_json()))


@bp_user.route('/', defaults={'user_id': None}, methods=['DELETE'])
@bp_user.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete(user_id):
    is_admin = get_jwt().get('is_admin')
    jwt_identity = get_jwt_identity()

    force_delete = False
    if user_id == jwt_identity and is_admin:

        if get_count_of_admin_users() > 1:
            force_delete = True
            return jsonify(delete_user(current_app, jwt_identity, force_delete))
        return resp_notallowed_user(
            msg=r"Você não pode excluir seu usuário administrador. "
                r"Crie uma conta de usuário e promova a administrador."
        )

    if is_admin and user_id != jwt_identity:
        force_delete = True
    result = delete_user(current_app, user_id, force_delete)
    response = jsonify(result[0])
    response.status_code = result[1]
    return response


@bp_user.route('/', methods=['PUT'])
@jwt_required()
def udpate():
    is_admin = get_jwt().get('is_admin')
    jwt_identity = get_jwt_identity()
    data = request.get_json()
    user_id = data.get('id')

    if is_admin:
        data.pop('active', '')
        if not (data.get('admin', True)):
            if get_count_of_admin_users() < 2:
                return resp_notallowed_user(
                    msg=r"Você não pode alterar seu status de usuário administrador para usuário comum. "
                        r"Promova algum administrador."
                )
    elif user_id != jwt_identity:
        return resp_notallowed_user()
    else:
        data.pop('admin', None)
    return jsonify(update_user(current_app, data))


@bp_user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authenticate(data)
