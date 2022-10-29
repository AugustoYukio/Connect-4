from . import (Blueprint, jwt_required, current_app, request, admin_required, owner_required)
from ..utils.themes import create_theme, find_theme, update_theme, delete_theme, find_themes_by_user

bp_theme = Blueprint('bp_theme', __name__, url_prefix='/theme')


@bp_theme.route('/', methods=['POST'])
@admin_required()
def create():
    data = request.get_json()
    return create_theme(current_app, data)


@bp_theme.route('/<theme_id>', methods=['GET'])
@jwt_required()
def get(theme_id):
    return find_theme(theme_id)


@bp_theme.route('/', methods=['GET'])
@owner_required()
def get_themes_by_user(user_id):
    """ Busca todos os temas incluindo os que o usuário já tem disponiveis"""
    return find_themes_by_user(user_id)


@bp_theme.route('/', methods=['PUT'])
@admin_required()
def update():
    data = request.get_json()
    return update_theme(current_app, data)


@bp_theme.route('/<theme_id>', methods=['DELETE'])
@admin_required()
def delete(theme_id):
    return delete_theme(current_app, theme_id)
