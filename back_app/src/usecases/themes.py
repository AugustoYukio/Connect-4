from . import (Blueprint, jwt_required, current_app, request, admin_required)
from back_app.src.utils.themes import create_theme, find_theme, update_theme, delete_theme

bp_theme = Blueprint('bp_theme', __name__, url_prefix='/theme')


@bp_theme.route('/', methods=['POST'])
@admin_required()
def create():
    data = request.get_json()
    return create_theme(current_app, data)


@bp_theme.route('/<chip_id>', methods=['GET'])
@jwt_required()
def get(chip_id):
    return find_theme(current_app, chip_id)


@bp_theme.route('/', methods=['PUT'])
@admin_required()
def update():
    data = request.get_json()
    return update_theme(current_app, data)


@bp_theme.route('/<board_id>', methods=['DELETE'])
@admin_required()
def delete(board_id):
    return delete_theme(current_app, board_id)
