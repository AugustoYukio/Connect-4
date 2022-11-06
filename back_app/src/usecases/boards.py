from . import (Blueprint, jwt_required, current_app, request, get_jwt, jsonify, resp_notallowed_user, admin_required)
from ..utils.boards import create_board, find_board, update_board, delete_board, find_all_board

bp_board = Blueprint('bp_board', __name__, url_prefix='/board')


@bp_board.route('/', methods=['POST'])
@admin_required()
def create():
    data = request.get_json()
    return jsonify(create_board(current_app, data))


@bp_board.route('/<chip_id>', methods=['GET'])
@jwt_required()
def get(chip_id):
    return find_board(chip_id)


@bp_board.route('/', methods=['GET'])
@jwt_required()
def get_all():
    page = request.args.get('page', 1, type=int)
    per_page = min(25, request.args.get('per_p', 25, type=int))

    return find_all_board(page, per_page)


@bp_board.route('/', methods=['PUT'])
@admin_required()
def update():
    data = request.get_json()
    return update_board(current_app, data)


@bp_board.route('/<board_id>', methods=['DELETE'])
@admin_required()
def delete(board_id):
    return delete_board(current_app, board_id)
