from . import (Blueprint, jwt_required, current_app, request)
from back_app.src.utils.boards import create_board, find_board, update_board, delete_board

bp_board = Blueprint('bp_board', __name__, url_prefix='/board')


@bp_board.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    return create_board(current_app, data)


@bp_board.route('/<chip_id>', methods=['GET'])
@jwt_required()
def get(chip_id):
    return find_board(current_app, chip_id)


@bp_board.route('/', methods=['PUT'])
@jwt_required()
def update():
    data = request.get_json()
    return update_board(current_app, data)


@bp_board.route('/<board_id>', methods=['DELETE'])
@jwt_required()
def delete(board_id):
    return delete_board(current_app, board_id)
