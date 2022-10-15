import jwt
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required

from ..utils.chips import create_chip, delete_chip, update_chip

bp_chip = Blueprint('bp_chip', __name__, url_prefix='/chip')


@bp_chip.route('/create', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    return create_chip(current_app, data)


@bp_chip.route('/delete', methods=['POST'])
@jwt_required()
def delete():
    data = request.get_json()
    return delete_chip(current_app, data)


@bp_chip.route('/update/<number>', methods=['POST'])
@jwt_required()
def update(number: str):
    data = request.get_json()
    return update_chip(current_app, data, number)
