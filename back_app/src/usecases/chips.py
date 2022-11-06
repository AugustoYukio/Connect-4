from . import (Blueprint, jwt_required, request, current_app, admin_required)
from ..utils.chips import (create_chip, delete_chip, update_chip, find_chip, find_all_chip)

bp_chip = Blueprint('bp_chip', __name__, url_prefix='/chip')


@bp_chip.route('/', methods=['POST'])
@admin_required()
def create():
    data = request.get_json()
    return create_chip(current_app, data)


@bp_chip.route('/<chip_id>', methods=['GET'])
@jwt_required()
def get(chip_id):
    return find_chip(chip_id)


@bp_chip.route('/', methods=['GET'])
@jwt_required()
def get_all():
    page = request.args.get('page', 1, type=int)
    per_page = min(25, request.args.get('per_p', 25, type=int))
    return find_all_chip(page, per_page)


@bp_chip.route('/', methods=['PUT'])
@admin_required()
def update():
    data = request.get_json()
    return update_chip(current_app, data)


@bp_chip.route('/<chip_id>', methods=['DELETE'])
@admin_required()
def delete(chip_id):
    return delete_chip(current_app, chip_id)
