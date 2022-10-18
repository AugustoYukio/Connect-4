from . import (Blueprint, jwt_required, request, current_app)
from back_app.src.utils.chips import (create_chip, delete_chip, update_chip, find_chip)

bp_chip = Blueprint('bp_chip', __name__, url_prefix='/chip')


@bp_chip.route('/', methods=['POST'])
@jwt_required()
def create():

    data = request.get_json()
    return create_chip(current_app, data)


@bp_chip.route('/<chip_id>', methods=['GET'])
@jwt_required()
def get(chip_id):
    return find_chip(current_app, chip_id)


@bp_chip.route('/', methods=['PUT'])
@jwt_required()
def update():
    data = request.get_json()
    return update_chip(current_app, data)


@bp_chip.route('/<chip_id>', methods=['DELETE'])
@jwt_required()
def delete(chip_id):

    return delete_chip(current_app, chip_id)
