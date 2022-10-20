
from . import (Blueprint, jwt_required, current_app, request, get_jwt, jsonify, resp_notallowed_user, admin_required)
from back_app.src.utils.boards import create_board, find_board, update_board, delete_board

bp_board = Blueprint('bp_board', __name__, url_prefix='/board')


@bp_board.route('/', methods=['POST'])
@admin_required()
def create():
    data = request.get_json()
    if get_jwt().get('is_admin'):
        return jsonify(create_board(current_app, data))
    return resp_notallowed_user()


@bp_board.route('/<chip_id>', methods=['GET'])
@jwt_required()
def get(chip_id):
    return find_board(current_app, chip_id)


@bp_board.route('/', methods=['PUT'])
@admin_required()
def update():
    data = request.get_json()
    return update_board(current_app, data)


@bp_board.route('/<board_id>', methods=['DELETE'])
@admin_required()
def delete(board_id):
    return delete_board(current_app, board_id)
